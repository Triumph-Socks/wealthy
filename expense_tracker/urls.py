from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expenses.api_views import (
    CategoryViewSet, ShopViewSet, ProductViewSet, ExpenseViewSet,
    PriceHistoryViewSet, BudgetViewSet,
    dashboard_stats, spending_trend, category_breakdown,
    price_analysis, shop_comparison, import_csv
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'shops', ShopViewSet)
router.register(r'products', ProductViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'price-history', PriceHistoryViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('api/dashboard/spending-trend/', spending_trend, name='spending-trend'),
    path('api/dashboard/category-breakdown/', category_breakdown, name='category-breakdown'),
    path('api/price-analysis/<int:product_id>/', price_analysis, name='price-analysis-detail'),
    path('api/shop-comparison/', shop_comparison, name='shop-comparison'),
    path('api/expenses/import-csv/', import_csv, name='import-csv'),
]
