from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='rest_tables'),  
    path('add_table', add_table, name='add-table'),  
    path('update_table/<int:id>', update_table, name='update-table'),
    path("delete_table/<int:id>/", delete_table, name="delete-table"),
    path('details/<int:id>/', show_table, name='show_table'),

]
