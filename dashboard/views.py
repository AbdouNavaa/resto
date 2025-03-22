from django.shortcuts import render
from dishes.models import Dish
from categories.models import Category
from coupons.models import Coupon
from users.models import User
from orders.models import Order
from order_items.models import OrderItem
from tables.models import Table
from datetime import datetime


# Create your views here.
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def index(request):
    # Vos autres requêtes...
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    coupons = Coupon.objects.all()
    users = User.objects.all()
    orders_in_progress = Order.objects.filter(status='قيد التنفيذ')
    today_orders = Order.objects.filter(created_at__date=timezone.now().date())
    total_price = today_orders.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    tables = Table.objects.all()

    # Récupérer les données mensuelles pour le graphique
    months_data = []
    for i in range(12):  # Les 12 derniers mois
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30 * i)
        month_end = month_start + timedelta(days=30)
        monthly_orders = Order.objects.filter(created_at__range=(month_start, month_end))
        total_orders = monthly_orders.count()
        total_revenue = monthly_orders.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
        months_data.append({
            'month': month_start.strftime('%Y-%m'),
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
        })

    months_data.reverse()  # Pour afficher du plus ancien au plus récent
    
    # tables
    tables = Table.objects.all()
    available_tables = Table.objects.filter(status='متاحة')
    busy_tables = Table.objects.filter(status='محجوزة')
    tables_data = []
    tables_data.append({
        'available_tables': available_tables.count(),
        'busy_tables': busy_tables.count(),
    })
    
    # print('Tables :',tables_data)
    
    # orders
    orders = Order.objects.all()
    delivery_orders = Order.objects.filter(order_type='delivery')
    take_out_orders = Order.objects.filter(order_type='take_out')
    dine_in_orders = Order.objects.filter(order_type='dine_in')
    orders_data = []
    orders_data.append({
        'delivery_orders': delivery_orders.count(),
        'take_out_orders': take_out_orders.count(),
        'dine_in_orders': dine_in_orders.count(),
    })
    # print('Orders :', orders_data)
    
    # categories
    categories = Category.objects.all()
    dishes_by_category = Dish.objects.values('category').annotate(count=Count('id')).order_by('-count')
    categories_data = []
    for category in categories:
        dishes_count = dishes_by_category.filter(category=category).first()['count']
        categories_data.append({
            'category': category.name,
            'dishes_count': dishes_count,
        })
    # print('Categories :', categories_data)
    
    # dishes in orders
    all_orders = OrderItem.objects.all()
    dishes_in_orders = []
    for order_item in all_orders:
        dish = order_item.dish
        if dish not in dishes_in_orders:
            dishes_in_orders.append(dish)
    dishes_in_orders_data = []
    for dish in dishes_in_orders:
        orders_count = all_orders.filter(dish=dish).count()
        dishes_in_orders_data.append({
            'dish': dish.name,
            'orders_count': orders_count,
        })
    # print('Dishes in orders :', dishes_in_orders_data)
    
    


    return render(request, 'index.html', {
        'dishes': dishes,
        'categories': categories,
        'coupons': coupons,
        'users': users,
        'today_orders': today_orders,
        'total_price':float(total_price),
        'orders_in_progress': orders_in_progress,
        'tables': tables,
        'months_data': months_data,  # Données pour le graphique
        'tables_data': tables_data,
        'orders_data': orders_data,
        'categories_data': categories_data,
        'dishes_in_orders_data': dishes_in_orders_data,  # Données pour le graphique
        
    })