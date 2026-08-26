from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, date
import csv
import io

from .models import Category, Shop, Product, Expense, PriceHistory, Budget
from .serializers import (
    CategorySerializer, ShopSerializer, ProductSerializer, 
    ExpenseSerializer, PriceHistorySerializer, BudgetSerializer,
    DashboardStatsSerializer, SpendingTrendSerializer, CategoryBreakdownSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('product', 'shop', 'product__category').all()
    serializer_class = ExpenseSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        shop = self.request.query_params.get('shop')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if category:
            queryset = queryset.filter(product__category_id=category)
        if shop:
            queryset = queryset.filter(shop_id=shop)
        if start_date:
            queryset = queryset.filter(purchase_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(purchase_date__lte=end_date)
            
        return queryset

class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.select_related('product', 'shop').all()
    serializer_class = PriceHistorySerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.select_related('category').all()
    serializer_class = BudgetSerializer

@api_view(['GET'])
def dashboard_stats(request):
    today = timezone.now().date()
    first_day_month = today.replace(day=1)
    
    total_expenses = Expense.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    this_month_expenses = Expense.objects.filter(
        purchase_date__gte=first_day_month
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    days_in_month = (today - first_day_month).days + 1
    avg_daily = this_month_expenses / days_in_month if days_in_month > 0 else 0
    
    categories_count = Category.objects.count()
    
    data = {
        'total_expenses': float(total_expenses),
        'this_month': float(this_month_expenses),
        'avg_daily': float(avg_daily),
        'categories_count': categories_count
    }
    
    serializer = DashboardStatsSerializer(data)
    return Response(serializer.data)

@api_view(['GET'])
def spending_trend(request):
    days = 30
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    labels = []
    data = []
    
    current = start_date
    while current <= end_date:
        expenses = Expense.objects.filter(
            purchase_date=current
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        labels.append(current.strftime('%b %d'))
        data.append(float(expenses))
        current += timedelta(days=1)
    
    result = {'labels': labels, 'data': data}
    serializer = SpendingTrendSerializer(result)
    return Response(serializer.data)

@api_view(['GET'])
def category_breakdown(request):
    breakdown = Expense.objects.values('product__category__name').annotate(
        total=Sum('total_price')
    ).order_by('-total')
    
    labels = [item['product__category__name'] for item in breakdown]
    data = [float(item['total']) for item in breakdown]
    
    result = {'labels': labels, 'data': data}
    serializer = CategoryBreakdownSerializer(result)
    return Response(serializer.data)

@api_view(['GET'])
def price_analysis(request, product_id):
    product = Product.objects.get(id=product_id)
    history = PriceHistory.objects.filter(product=product).select_related('shop').order_by('recorded_date')
    
    labels = []
    datasets = {}
    
    for record in history:
        shop_name = record.shop.name
        if shop_name not in datasets:
            datasets[shop_name] = []
        labels.append(record.recorded_date.strftime('%b %d'))
        datasets[shop_name].append(float(record.price_per_unit))
    
    return Response({
        'product': ProductSerializer(product).data,
        'labels': labels,
        'datasets': datasets
    })

@api_view(['GET'])
def shop_comparison(request):
    products = Product.objects.all()
    comparison = []
    
    for product in products:
        shops_data = Expense.objects.filter(product=product).values('shop__name').annotate(
            avg_price=Avg('price_per_unit'),
            min_price=Min('price_per_unit'),
            max_price=Max('price_per_unit'),
            count=Count('id')
        ).order_by('avg_price')
        
        if len(shops_data) > 1:
            best_shop = shops_data.first()
            worst_shop = shops_data.last()
            savings = float(worst_shop['avg_price']) - float(best_shop['avg_price'])
            
            comparison.append({
                'product': product.name,
                'best_shop': best_shop['shop__name'],
                'best_price': float(best_shop['avg_price']),
                'worst_shop': worst_shop['shop__name'],
                'worst_price': float(worst_shop['avg_price']),
                'savings': savings,
                'shops': list(shops_data)
            })
    
    return Response(comparison)

@api_view(['POST'])
def import_csv(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = request.FILES['file']
    decoded_file = csv_file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)
    
    created_count = 0
    errors = []
    
    for row_num, row in enumerate(reader, start=2):
        try:
            # Expected columns: product_name, shop_name, quantity, price_per_unit, purchase_date, notes
            product_name = row.get('product_name', '').strip()
            shop_name = row.get('shop_name', '').strip()
            quantity = row.get('quantity', '1').strip()
            price_per_unit = row.get('price_per_unit', '0').strip()
            purchase_date = row.get('purchase_date', '').strip()
            notes = row.get('notes', '').strip()
            
            if not product_name or not shop_name:
                errors.append(f"Row {row_num}: Missing product_name or shop_name")
                continue
            
            # Get or create product and shop
            category, _ = Category.objects.get_or_create(name='Imported')
            product, _ = Product.objects.get_or_create(
                name=product_name,
                defaults={'category': category, 'unit': 'piece'}
            )
            shop, _ = Shop.objects.get_or_create(name=shop_name)
            
            # Parse date
            from datetime import datetime
            if purchase_date:
                parsed_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()
            else:
                parsed_date = timezone.now().date()
            
            # Create expense
            Expense.objects.create(
                product=product,
                shop=shop,
                quantity=decimal.Decimal(quantity),
                price_per_unit=decimal.Decimal(price_per_unit),
                purchase_date=parsed_date,
                notes=notes
            )
            created_count += 1
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return Response({
        'created': created_count,
        'errors': errors[:10]  # Return first 10 errors
    })

# Import decimal for CSV parsing
from decimal import Decimal as decimal
from django.db.models import Min, Max
