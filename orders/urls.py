from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', order_list, name='order_list'),
    path('search/', csrf_exempt(search), name='search-orders'),   
    path('items/<int:order_id>/', get_order_items, name='get_order_items'),
    path('update/<int:order_id>/', update_order, name='update_order'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
]
