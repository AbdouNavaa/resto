from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='dishes'),   
    path('search/', csrf_exempt(views.search), name='search-dishes'),   
    path('add_dishe', csrf_exempt(views.add_dishe), name='add-dishe'),   
    path('update_dish/<int:id>', csrf_exempt(views.update_dish), name='update-dishe'),  
    path("delete/<int:id>/", views.delete_dish, name="delete-dishe"),
    path('export_to_excel', csrf_exempt(views.export_to_excel), name='export_to_excel'),   
    path('export_to_pdf', csrf_exempt(views.export_to_pdf), name='export_to_pdf'),   
    

]

