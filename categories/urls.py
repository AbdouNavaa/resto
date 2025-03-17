from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='categories'),   
    path('add_category/', views.add_category, name='add-category'),
    path('edit_category/<int:id>/', views.update_category, name='update-category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete-category'),
    path('search', csrf_exempt(views.search), name='search-categories'),   
    
]
