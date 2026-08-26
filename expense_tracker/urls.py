from django.contrib import admin
from django.urls import path
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='expense_add'),
    path('expenses/<int:expense_id>/delete/', views.delete_expense, name='expense_delete'),
    path('expenses/import-csv/', views.import_csv, name='import_csv'),
    path('price-analysis/', views.price_analysis, name='price_analysis'),
    path('shop-comparison/', views.shop_comparison, name='shop_comparison'),
    path('category-report/', views.category_report, name='category_report'),
    path('api/products/', views.get_products_json, name='api_products'),
    path('api/shops/', views.get_shops_json, name='api_shops'),
]
