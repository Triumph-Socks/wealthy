from django.core.management.base import BaseCommand
from expenses.models import Category, Shop, Product, Budget
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Groceries', 'description': 'Food and household items', 'budget_limit': Decimal('500.00')},
            {'name': 'Utilities', 'description': 'Electricity, water, gas, internet', 'budget_limit': Decimal('200.00')},
            {'name': 'Transportation', 'description': 'Fuel, public transport, maintenance', 'budget_limit': Decimal('300.00')},
            {'name': 'Entertainment', 'description': 'Movies, dining out, hobbies', 'budget_limit': Decimal('150.00')},
            {'name': 'Healthcare', 'description': 'Medicine, doctor visits', 'budget_limit': Decimal('100.00')},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, _ = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            self.stdout.write(f'Created category: {category.name}')
        
        # Create shops
        shops_data = [
            {'name': 'Walmart', 'shop_type': 'Supermarket', 'rating': Decimal('4.2')},
            {'name': 'Target', 'shop_type': 'Supermarket', 'rating': Decimal('4.3')},
            {'name': 'Costco', 'shop_type': 'Warehouse', 'rating': Decimal('4.5')},
            {'name': 'Whole Foods', 'shop_type': 'Organic Grocery', 'rating': Decimal('4.4')},
            {'name': 'Shell Gas Station', 'shop_type': 'Gas Station', 'rating': Decimal('4.0')},
            {'name': 'CVS Pharmacy', 'shop_type': 'Pharmacy', 'rating': Decimal('4.1')},
            {'name': 'Amazon Fresh', 'shop_type': 'Online Grocery', 'rating': Decimal('4.2')},
        ]
        
        shops = {}
        for shop_data in shops_data:
            shop, _ = Shop.objects.get_or_create(
                name=shop_data['name'],
                defaults=shop_data
            )
            shops[shop.name] = shop
            self.stdout.write(f'Created shop: {shop.name}')
        
        # Create products
        products_data = [
            {'name': 'Milk', 'category': 'Groceries', 'unit': 'liter'},
            {'name': 'Bread', 'category': 'Groceries', 'unit': 'loaf'},
            {'name': 'Eggs', 'category': 'Groceries', 'unit': 'dozen'},
            {'name': 'Rice', 'category': 'Groceries', 'unit': 'kg'},
            {'name': 'Chicken Breast', 'category': 'Groceries', 'unit': 'kg'},
            {'name': 'Bananas', 'category': 'Groceries', 'unit': 'kg'},
            {'name': 'Gasoline', 'category': 'Transportation', 'unit': 'liter'},
            {'name': 'Bus Pass', 'category': 'Transportation', 'unit': 'month'},
            {'name': 'Electricity', 'category': 'Utilities', 'unit': 'kWh'},
            {'name': 'Internet', 'category': 'Utilities', 'unit': 'month'},
            {'name': 'Movie Ticket', 'category': 'Entertainment', 'unit': 'ticket'},
            {'name': 'Restaurant Meal', 'category': 'Entertainment', 'unit': 'meal'},
            {'name': 'Pain reliever', 'category': 'Healthcare', 'unit': 'box'},
        ]
        
        products = {}
        for prod_data in products_data:
            product, _ = Product.objects.get_or_create(
                name=prod_data['name'],
                category=categories[prod_data['category']],
                defaults={'unit': prod_data['unit']}
            )
            products[product.name] = product
            self.stdout.write(f'Created product: {product.name}')
        
        # Create budgets for current month
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        for cat_name, category in categories.items():
            budget_amount = category.budget_limit
            budget, created = Budget.objects.get_or_create(
                category=category,
                month=current_month,
                year=current_year,
                defaults={'amount': budget_amount}
            )
            if created:
                self.stdout.write(f'Created budget for {cat_name}: ${budget_amount}')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with sample data!'))
