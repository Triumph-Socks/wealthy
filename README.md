# Expense Tracker - Django Web Application

A comprehensive expense tracking web application built with Django that helps you track expenses, monitor price fluctuations, analyze inflation, and make smart shopping decisions.

## Features

### Core Features
- **Expense Tracking**: Record all your purchases with product, shop, quantity, and price details
- **Price History**: Automatically track price changes over time to monitor inflation
- **Shop Comparison**: Compare prices across different shops to find the best deals
- **Category Management**: Organize expenses into customizable categories
- **Budget Tracking**: Set monthly budgets per category and track spending against them
- **Dashboard Analytics**: Visual insights with charts and statistics

### Additional Features
- Modern, responsive UI with Bootstrap 5
- Interactive charts using Chart.js
- Filter expenses by category, shop, and date range
- Price trend analysis for individual products
- Smart recommendations for best shops per product
- Admin panel for data management

## Tech Stack

- **Backend**: Django 6.1
- **Database**: SQLite (default)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js
- **Icons**: Bootstrap Icons

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd /workspace
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Seed the database with sample data** (optional but recommended)
   ```bash
   python manage.py seed_data
   ```

5. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

7. **Access the application**
   - Main Dashboard: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Project Structure

```
/workspace/
├── expense_tracker/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── expenses/              # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── admin.py           # Admin configurations
│   ├── templates/         # HTML templates
│   │   └── expenses/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── expense_list.html
│   │       ├── add_expense.html
│   │       ├── price_analysis.html
│   │       ├── shop_comparison.html
│   │       └── category_report.html
│   └── management/        # Custom management commands
│       └── commands/
│           └── seed_data.py
├── manage.py
└── db.sqlite3
```

## Data Models

- **Category**: Expense categories with budget limits
- **Shop**: Stores/shops where purchases are made
- **Product**: Items that can be purchased
- **Expense**: Individual purchase records
- **PriceHistory**: Historical price data for inflation tracking
- **Budget**: Monthly budget allocations per category

## Usage Guide

### Adding Expenses
1. Navigate to "Add Expense" from the sidebar
2. Select product and shop
3. Enter quantity and price per unit
4. Add optional notes
5. Save - price history is automatically recorded

### Analyzing Prices
1. Go to "Price Analysis" page
2. Select a product to view its price history
3. Compare prices across different shops
4. Track inflation over time

### Shop Comparison
1. Visit "Shop Comparison" page
2. View which shop offers the best price for each product
3. See potential savings by shopping at the right place

### Budget Management
1. Use the admin panel to set monthly budgets
2. Monitor budget vs actual spending on the dashboard
3. Get visual alerts when approaching budget limits

## Admin Panel

Access the admin panel at `/admin/` to:
- Manage categories, shops, and products
- View and edit all expense records
- Configure budgets
- Analyze price history data

## Screenshots

The application includes:
- Modern dashboard with spending statistics
- Interactive charts for trends and categories
- Budget progress bars with color-coded alerts
- Responsive tables for expense listings
- Price comparison views

## License

This project is open source and available for educational and commercial use.
