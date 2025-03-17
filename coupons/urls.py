from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='coupons'),  
    path('add_coupon/', views.create, name='add-coupon'), 
    path('update_coupon/<int:id>/', views.update, name='update-coupon'), 
    path('delete_coupon/<int:id>/', views.delete, name='delete-coupon'), 

]
