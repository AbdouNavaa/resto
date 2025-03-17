from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='point_of_sale'),
    path('remove_dish/<int:dish_id>/', views.remove_dish, name='remove_dish'),
    path('clear_order/', views.clear_order, name='clear_order'),
    path('update_quantity/<int:dish_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('create_order/', views.create_order, name='create_order'),
]
