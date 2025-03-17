from django.shortcuts import render
from dishes.models import Dish
from categories.models import Category
from coupons.models import Coupon
from users.models import User
from orders.models import Order
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
    })