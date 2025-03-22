from django.shortcuts import render, redirect
from .models import *
from dishes.models import Dish
import json
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
# Create your views here.
from django.db.models import Count
from django.core.paginator import Paginator

def index(request):
    tables = Table.objects.all()
    paginator = Paginator(tables, 5)  # Show 5 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tables/index.html', {'tables': page_obj,'page_obj': page_obj,})
# search


# def search(request):
#     if request.method == 'POST':
#         query = json.loads(request.body).get('query')
#         tables = Table.objects.filter(number__icontains=query) 
#         data = categories.values()
#         return JsonResponse(list(data), safe=False)

# show
from django.core import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
from orders.models import Order
from order_items.models import OrderItem

def show_table(request, id):
    table = Table.objects.get(pk=id)
    if table.status == 'محجوزة':
        order = Order.objects.get(table=table)
        order_items = OrderItem.objects.filter(order=order)
        items_data = [{
            'dish__name': item.dish.name,
            'quantity': item.quantity,
            'price': float(item.price),
        } for item in order_items]
        print(table)
        print(order)
        print(order_items)

        # Récupérer les informations de la commande
        order_data = {
            'id': order.id,
            'user': order.user.username,
            'order_type': order.get_order_type_display(),
            'status': order.get_status_display(),
            'total_price': float(order.total_price),
            'created_at': order.created_at.strftime("%d/%m/%Y %H:%M"),
            'delivery_address': order.delivery_address,
            'phone_number': order.phone_number,
            'pickup_time': order.pickup_time.strftime("%d/%m/%Y %H:%M") if order.pickup_time else None,
            'table': order.table.id if order.table else None,
        }

        return JsonResponse({
            'order_items': items_data,
            'order': order_data,
        })
    else:
        # messages.error(request,'الطاولة ليست محجوزة')
        return JsonResponse({'order_items': [], 'order': {}})

# add

def add_table(request):
    tables = Table.objects.all() 
    # status = ['م']
    context = {'tables': tables, 'values': request.POST}
    
    if request.method == 'GET':
        return render(request, 'tables/add_table.html', context)
    
    if request.method == 'POST':
        number = request.POST['number']
        number_of_seats = request.POST['number_of_seats']
        status = request.POST['status']

        # Validation des champs obligatoires
        if  not number or not number_of_seats:
            messages.error(request, 'الرجاء تعبئة جميع الحقول')
            return render(request, 'tables/add_table.html', context)

        # Créer l'objet table
        Table.objects.create(
            number=number,
            number_of_seats=number_of_seats,
            status=status,  # Assigner l'instance de table
        )

        messages.success(request, 'تمت الاضافة بنجاح')
        return redirect('rest_tables')

def update_table(request,id):
    table = Table.objects.get(pk=id)
    context = {'table': table, 'values': table}
    
    if request.method == 'GET':
        return render(request, 'tables/edit_table.html', context)
    
    if request.method == 'POST':
        number = request.POST['number']
        number_of_seats = request.POST['number_of_seats']
        status = request.POST['status']

        # Validation des champs obligatoires
        if not number or not number_of_seats:
            messages.error(request, 'الرجاء تعبئة جميع الحقول')
            return render(request, 'tables/edit_table.html', context)



        # Créer l'objet table
        table.number=number
        table.number_of_seats=number_of_seats
        table.status=status
        table.save()

        messages.success(request, ' تم التعديل بنجاح')
        return redirect('rest_tables')

# delete

def delete_table(request,id):
    table = Table.objects.get(pk=id)
    table.delete()
    messages.success(request, ' تم الحذف بنجاح')
    return redirect('rest_tables')
