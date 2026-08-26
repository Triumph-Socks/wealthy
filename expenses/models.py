from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Expense categories like Groceries, Utilities, Transportation, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Shops/stores where purchases are made."""
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    shop_type = models.CharField(max_length=100, blank=True)  # e.g., Grocery, Electronics, Restaurant
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text="Rating out of 5")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Products/items that can be purchased."""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    unit = models.CharField(max_length=50, default='piece', help_text="e.g., kg, liter, piece")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Expense(models.Model):
    """Individual expense records."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='expenses')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='expenses')
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date', '-created_at']

    def __str__(self):
        return f"{self.product.name} at {self.shop.name} - ${self.total_price}"

    def save(self, *args, **kwargs):
        # Auto-calculate total_price
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)


class PriceHistory(models.Model):
    """Track price history for products at different shops to monitor inflation."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='price_history')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_date']
        unique_together = ['product', 'shop', 'recorded_date']

    def __str__(self):
        return f"{self.product.name} at {self.shop.name} - ${self.price_per_unit} on {self.recorded_date}"


class Budget(models.Model):
    """Monthly budget tracking."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    month = models.IntegerField(help_text="1-12")
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['category', 'month', 'year']

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year} - ${self.amount}"
