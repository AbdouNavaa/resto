from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='users'),
    path('add_user/', views.create, name='add-user'),   
    path('update_user/<int:pk>', views.update, name='update-user'),
    path('delete_user/<int:pk>', views.delete, name='delete-user'),
    path('login/', views.login, name='login'),
]
