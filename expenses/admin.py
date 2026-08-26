from django.contrib import admin
from .models import Category, Shop, Product, Expense, PriceHistory, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget_limit', 'created_at']
    search_fields = ['name']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop_type', 'rating', 'created_at']
    list_filter = ['shop_type']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'created_at']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['product', 'shop', 'quantity', 'price_per_unit', 'total_price', 'purchase_date']
    list_filter = ['purchase_date', 'shop', 'product__category']
    search_fields = ['product__name', 'shop__name']
    date_hierarchy = 'purchase_date'


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'shop', 'price_per_unit', 'recorded_date']
    list_filter = ['recorded_date', 'shop', 'product__category']
    search_fields = ['product__name', 'shop__name']
    date_hierarchy = 'recorded_date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'month', 'year', 'amount']
    list_filter = ['year', 'month', 'category']
