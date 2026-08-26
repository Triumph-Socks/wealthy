from django.core.management.base import BaseCommand
from expenses.models import Category, Shop, Product, Budget, Expense, PriceHistory
from decimal import Decimal
from datetime import datetime, timedelta
import random


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
        
        # Create sample expenses with price history
        expense_configs = [
            {'product': 'Milk', 'shop': 'Walmart', 'base_price': Decimal('1.29'), 'quantity': 2},
            {'product': 'Milk', 'shop': 'Whole Foods', 'base_price': Decimal('1.89'), 'quantity': 1},
            {'product': 'Milk', 'shop': 'Costco', 'base_price': Decimal('1.15'), 'quantity': 4},
            {'product': 'Bread', 'shop': 'Walmart', 'base_price': Decimal('2.49'), 'quantity': 2},
            {'product': 'Bread', 'shop': 'Target', 'base_price': Decimal('2.79'), 'quantity': 1},
            {'product': 'Eggs', 'shop': 'Walmart', 'base_price': Decimal('3.99'), 'quantity': 2},
            {'product': 'Eggs', 'shop': 'Costco', 'base_price': Decimal('4.29'), 'quantity': 3},
            {'product': 'Rice', 'shop': 'Walmart', 'base_price': Decimal('5.49'), 'quantity': 1},
            {'product': 'Rice', 'shop': 'Amazon Fresh', 'base_price': Decimal('4.99'), 'quantity': 2},
            {'product': 'Chicken Breast', 'shop': 'Walmart', 'base_price': Decimal('8.99'), 'quantity': 1},
            {'product': 'Chicken Breast', 'shop': 'Whole Foods', 'base_price': Decimal('12.99'), 'quantity': 1},
            {'product': 'Bananas', 'shop': 'Walmart', 'base_price': Decimal('1.99'), 'quantity': 2},
            {'product': 'Bananas', 'shop': 'Target', 'base_price': Decimal('2.29'), 'quantity': 1},
            {'product': 'Gasoline', 'shop': 'Shell Gas Station', 'base_price': Decimal('3.49'), 'quantity': 40},
            {'product': 'Bus Pass', 'shop': 'City Transit', 'base_price': Decimal('75.00'), 'quantity': 1},
            {'product': 'Electricity', 'shop': 'Power Company', 'base_price': Decimal('0.12'), 'quantity': 800},
            {'product': 'Internet', 'shop': 'Comcast', 'base_price': Decimal('69.99'), 'quantity': 1},
            {'product': 'Movie Ticket', 'shop': 'AMC Theater', 'base_price': Decimal('15.99'), 'quantity': 2},
            {'product': 'Restaurant Meal', 'shop': 'Local Diner', 'base_price': Decimal('25.00'), 'quantity': 2},
            {'product': 'Pain reliever', 'shop': 'CVS Pharmacy', 'base_price': Decimal('8.99'), 'quantity': 1},
        ]
        
        # Create shops for additional vendors
        additional_shops = ['City Transit', 'Power Company', 'Comcast', 'AMC Theater', 'Local Diner']
        for shop_name in additional_shops:
            if shop_name not in shops:
                shop, _ = Shop.objects.get_or_create(
                    name=shop_name,
                    defaults={'shop_type': 'Other', 'rating': Decimal('4.0')}
                )
                shops[shop_name] = shop
        
        today = datetime.now()
        expenses_created = 0
        
        for config in expense_configs:
            product = products.get(config['product'])
            shop = shops.get(config['shop'])
            
            if not product or not shop:
                continue
            
            # Create multiple historical prices (going back 3 months)
            for weeks_ago in range(12, 0, -1):
                expense_date = today - timedelta(weeks=weeks_ago)
                # Add some price variation over time (inflation simulation)
                inflation_factor = Decimal('1.0') + (Decimal('0.005') * (12 - weeks_ago))
                price = config['base_price'] * inflation_factor
                # Add small random variation
                price_variation = Decimal(str(random.uniform(0.95, 1.05)))
                final_price = (price * price_variation).quantize(Decimal('0.01'))
                
                expense, created = Expense.objects.get_or_create(
                    product=product,
                    shop=shop,
                    purchase_date=expense_date.date(),
                    defaults={
                        'quantity': Decimal(str(config['quantity'])),
                        'price_per_unit': final_price,
                        'notes': f'Sample expense from {weeks_ago} weeks ago'
                    }
                )
                
                if created:
                    expenses_created += 1
                    # Create price history entry
                    PriceHistory.objects.get_or_create(
                        product=product,
                        shop=shop,
                        recorded_date=expense_date.date(),
                        defaults={'price_per_unit': final_price}
                    )
        
        # Create recent expenses (last few days)
        recent_products = ['Milk', 'Bread', 'Eggs', 'Gasoline', 'Bananas']
        for i, prod_name in enumerate(recent_products):
            product = products.get(prod_name)
            if not product:
                continue
            
            shop = list(shops.values())[i % len(shops)]
            expense_date = today - timedelta(days=i)
            
            expense, created = Expense.objects.get_or_create(
                product=product,
                shop=shop,
                purchase_date=expense_date.date(),
                defaults={
                    'quantity': Decimal(str(random.randint(1, 3))),
                    'price_per_unit': Decimal(str(round(random.uniform(2, 10), 2))),
                    'notes': 'Recent purchase'
                }
            )
            
            if created:
                expenses_created += 1
                PriceHistory.objects.get_or_create(
                    product=product,
                    shop=shop,
                    recorded_date=expense_date.date(),
                    defaults={'price_per_unit': expense.price_per_unit}
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {expenses_created} sample expenses!'))
