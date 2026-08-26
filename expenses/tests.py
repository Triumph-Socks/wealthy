from django.test import TestCase, Client
from django.urls import reverse
from expenses.models import Category, Shop, Product, Expense


class ModelsTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Groceries')
        self.assertEqual(str(category), 'Groceries')
    
    def test_shop_creation(self):
        shop = Shop.objects.create(name='Walmart')
        self.assertEqual(str(shop), 'Walmart')
    
    def test_product_creation(self):
        category = Category.objects.create(name='Groceries')
        product = Product.objects.create(name='Milk', category=category, unit='gallon')
        self.assertIn('Milk', str(product))
        self.assertEqual(product.unit, 'gallon')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Groceries')
        self.shop = Shop.objects.create(name='Walmart')
        self.product = Product.objects.create(name='Milk', category=self.category, unit='gallon')
        self.expense = Expense.objects.create(
            product=self.product,
            shop=self.shop,
            quantity=2,
            price_per_unit=3.99
        )
    
    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_expense_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('expenses', response.context)
    
    def test_add_expense_view_get(self):
        response = self.client.get(reverse('expense_add'))
        self.assertEqual(response.status_code, 200)
    
    def test_add_expense_view_post(self):
        data = {
            'product': self.product.id,
            'shop': self.shop.id,
            'quantity': 1,
            'price_per_unit': 5.99,
            'purchase_date': '2024-01-15',
            'notes': ''
        }
        response = self.client.post(reverse('expense_add'), data)
        self.assertEqual(response.status_code, 302)
    
    def test_delete_expense_view(self):
        expense_id = self.expense.id
        response = self.client.post(reverse('expense_delete', args=[expense_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(id=expense_id).exists())
    
    def test_price_analysis_view(self):
        response = self.client.get(reverse('price_analysis'))
        self.assertEqual(response.status_code, 200)
    
    def test_shop_comparison_view(self):
        response = self.client.get(reverse('shop_comparison'))
        self.assertEqual(response.status_code, 200)
    
    def test_category_report_view(self):
        response = self.client.get(reverse('category_report'))
        self.assertEqual(response.status_code, 200)
    
    def test_import_csv_view(self):
        response = self.client.get(reverse('import_csv'))
        self.assertEqual(response.status_code, 302)


class APITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Groceries')
        self.shop = Shop.objects.create(name='Walmart')
        self.product = Product.objects.create(name='Milk', category=self.category, unit='gallon')
    
    def test_get_products_json(self):
        response = self.client.get(reverse('api_products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
    
    def test_get_shops_json(self):
        response = self.client.get(reverse('api_shops'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
