from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, Count, Q, F
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Shop, Product, Expense, PriceHistory, Budget


def dashboard(request):
    """Main dashboard with expense overview and analytics."""
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Total expenses this month
    monthly_expenses = Expense.objects.filter(
        purchase_date__month=current_month,
        purchase_date__year=current_year
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Total expenses this year
    yearly_expenses = Expense.objects.filter(
        purchase_date__year=current_year
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Expenses by category (this month)
    expenses_by_category = Category.objects.annotate(
        total_spent=Sum('products__expenses__total_price', 
                       filter=Q(products__expenses__purchase_date__month=current_month,
                               products__expenses__purchase_date__year=current_year))
    ).order_by('-total_spent')[:5]
    
    # Top shops by spending
    top_shops = Shop.objects.annotate(
        total_spent=Sum('expenses__total_price',
                       filter=Q(expenses__purchase_date__month=current_month,
                               expenses__purchase_date__year=current_year))
    ).order_by('-total_spent')[:5]
    
    # Recent expenses
    recent_expenses = Expense.objects.select_related('product', 'shop', 'product__category').order_by('-purchase_date')[:10]
    
    # Budget vs Actual for current month
    budget_data = []
    for category in Category.objects.all():
        budget = Budget.objects.filter(
            category=category,
            month=current_month,
            year=current_year
        ).first()
        
        actual = Expense.objects.filter(
            product__category=category,
            purchase_date__month=current_month,
            purchase_date__year=current_year
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        if budget:
            budget_data.append({
                'category': category,
                'budget': budget.amount,
                'actual': actual,
                'percentage': (actual / budget.amount * 100) if budget.amount > 0 else 0
            })
    
    # Monthly trend (last 6 months)
    six_months_ago = today - timedelta(days=180)
    monthly_trend = Expense.objects.filter(
        purchase_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('purchase_date')
    ).values('month').annotate(
        total=Sum('total_price')
    ).order_by('month')
    
    context = {
        'monthly_expenses': monthly_expenses,
        'yearly_expenses': yearly_expenses,
        'expenses_by_category': expenses_by_category,
        'top_shops': top_shops,
        'recent_expenses': recent_expenses,
        'budget_data': budget_data,
        'monthly_trend': monthly_trend,
        'current_month_name': today.strftime('%B'),
        'current_year': current_year,
    }
    
    return render(request, 'expenses/dashboard.html', context)


def expense_list(request):
    """List all expenses with filtering options."""
    expenses = Expense.objects.select_related('product', 'shop', 'product__category').order_by('-purchase_date')
    
    # Filters
    category_id = request.GET.get('category')
    shop_id = request.GET.get('shop')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if category_id:
        expenses = expenses.filter(product__category_id=category_id)
    if shop_id:
        expenses = expenses.filter(shop_id=shop_id)
    if start_date:
        expenses = expenses.filter(purchase_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(purchase_date__lte=end_date)
    
    categories = Category.objects.all()
    shops = Shop.objects.all()
    products = Product.objects.select_related('category').order_by('name')
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'shops': shops,
        'products': products,
    }
    
    return render(request, 'expenses/expense_list.html', context)


def add_expense(request):
    """Add a new expense."""
    if request.method == 'POST':
        product_id = request.POST.get('product')
        shop_id = request.POST.get('shop')
        quantity = request.POST.get('quantity')
        price_per_unit = request.POST.get('price_per_unit')
        purchase_date = request.POST.get('purchase_date')
        notes = request.POST.get('notes')
        
        product = get_object_or_404(Product, id=product_id)
        shop = get_object_or_404(Shop, id=shop_id)
        
        expense = Expense.objects.create(
            product=product,
            shop=shop,
            quantity=quantity,
            price_per_unit=price_per_unit,
            purchase_date=purchase_date or timezone.now().date(),
            notes=notes
        )
        
        # Create/update price history
        PriceHistory.objects.create(
            product=product,
            shop=shop,
            price_per_unit=price_per_unit,
            recorded_date=purchase_date or timezone.now().date()
        )
        
        return redirect('expense_list')
    
    products = Product.objects.select_related('category').order_by('name')
    shops = Shop.objects.order_by('name')
    
    context = {
        'products': products,
        'shops': shops,
    }
    
    return render(request, 'expenses/add_expense.html', context)


def price_analysis(request):
    """Analyze price fluctuations and inflation."""
    products = Product.objects.all()
    selected_product = None
    price_data = []
    
    product_id = request.GET.get('product')
    if product_id:
        selected_product = get_object_or_404(Product, id=product_id)
        price_history = PriceHistory.objects.filter(
            product=selected_product
        ).select_related('shop').order_by('recorded_date')
        
        # Group by shop
        shops_data = {}
        for record in price_history:
            if record.shop.name not in shops_data:
                shops_data[record.shop.name] = []
            shops_data[record.shop.name].append({
                'date': record.recorded_date,
                'price': float(record.price_per_unit)
            })
        
        price_data = shops_data
    
    context = {
        'products': products,
        'selected_product': selected_product,
        'price_data': price_data,
    }
    
    return render(request, 'expenses/price_analysis.html', context)


def shop_comparison(request):
    """Compare shops for best prices on products."""
    shops = Shop.objects.all()
    comparisons = []
    
    # Get products with prices at multiple shops
    products = Product.objects.annotate(
        shop_count=Count('price_history__shop', distinct=True)
    ).filter(shop_count__gt=1)
    
    for product in products[:20]:  # Limit to 20 products
        price_history = PriceHistory.objects.filter(
            product=product
        ).select_related('shop').order_by('-recorded_date')
        
        # Get latest price per shop
        latest_prices = {}
        for record in price_history:
            if record.shop.name not in latest_prices:
                latest_prices[record.shop.name] = float(record.price_per_unit)
        
        if len(latest_prices) > 1:
            min_price = min(latest_prices.values())
            max_price = max(latest_prices.values())
            best_shop = [name for name, price in latest_prices.items() if price == min_price][0]
            
            comparisons.append({
                'product': product,
                'prices': latest_prices,
                'min_price': min_price,
                'max_price': max_price,
                'best_shop': best_shop,
                'savings': max_price - min_price
            })
    
    context = {
        'shops': shops,
        'comparisons': comparisons,
    }
    
    return render(request, 'expenses/shop_comparison.html', context)


def category_report(request):
    """Detailed report by category."""
    categories = Category.objects.all()
    selected_category = None
    expenses = None
    total = 0
    
    category_id = request.GET.get('category')
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        expenses = Expense.objects.filter(
            product__category=selected_category
        ).select_related('product', 'shop').order_by('-purchase_date')
        total = expenses.aggregate(sum=Sum('total_price'))['sum'] or 0
    
    context = {
        'categories': categories,
        'selected_category': selected_category,
        'expenses': expenses,
        'total': total,
    }
    
    return render(request, 'expenses/category_report.html', context)


def delete_expense(request, expense_id):
    """Delete an expense."""
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('expense_list')
