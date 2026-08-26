from rest_framework import serializers
from .models import Category, Shop, Product, Expense, PriceHistory, Budget

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'budget_limit', 'created_at']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'shop_type', 'rating', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'unit', 'created_at']

class ExpenseSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    category = serializers.IntegerField(source='product.category.id', read_only=True)
    
    class Meta:
        model = Expense
        fields = ['id', 'product', 'product_name', 'shop', 'shop_name', 'category', 
                  'quantity', 'price_per_unit', 'total_price', 'purchase_date', 'notes', 'created_at']

class PriceHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    
    class Meta:
        model = PriceHistory
        fields = ['id', 'product', 'product_name', 'shop', 'shop_name', 'price_per_unit', 'recorded_date', 'created_at']

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'month', 'year', 'amount', 'created_at']

class DashboardStatsSerializer(serializers.Serializer):
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    this_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    avg_daily = serializers.DecimalField(max_digits=12, decimal_places=2)
    categories_count = serializers.IntegerField()

class SpendingTrendSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))

class CategoryBreakdownSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
