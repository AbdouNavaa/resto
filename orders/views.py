from django.shortcuts import render, redirect
from .models import Order
from order_items.models import OrderItem
from django.contrib import messages

def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    selected_order_id = request.GET.get('order_id')

    if selected_order_id:
        order_items = OrderItem.objects.filter(order_id=selected_order_id).select_related('dish').values(
            'dish__name', 'quantity', 'price'
        )

        # Convertir Decimal en float
        order_items = [
            {'dish__name': item['dish__name'], 'quantity': item['quantity'], 'price': float(item['price'])}
            for item in order_items
        ]

        print("Order Items:", order_items,selected_order_id)  # Debugging
    else:
        order_items = []

    paginator = Paginator(orders, 5)  # Show 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)        
    return render(request, 'orders/index.html', {
    'orders': page_obj,
    'page_obj': page_obj,  # Déjà converti en liste de dictionnaires
    'order_items': order_items,  # Déjà converti en liste de dictionnaires
    'selected_order_id': selected_order_id
    })

from django.core.paginator import Paginator

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        orders = Order.objects.filter(user__username__icontains=query) 
        selected_order_id = request.GET.get('order_id')

        if selected_order_id:
            order_items = OrderItem.objects.filter(order_id=selected_order_id).select_related('dish').values(
                'dish__name', 'quantity', 'price'
            )

            # Convertir Decimal en float
            order_items = [
                {'dish__name': item['dish__name'], 'quantity': item['quantity'], 'price': float(item['price'])}
                for item in order_items
            ]

            print("Order Items:", order_items,selected_order_id)  # Debugging
        else:
            order_items = []
        if not orders:
            messages.error(request, 'لا يوجد نتائج')
            return redirect('order_list')
        paginator = Paginator(orders, 5)  # Show 5 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        return render(request, 'orders/index.html', {
        'orders': page_obj,
        'page_obj': page_obj,  # Déjà converti en liste de dictionnaires
        'order_items': order_items,  # Déjà converti en liste de dictionnaires
        'selected_order_id': selected_order_id
    })
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse
from orders.models import Order
from order_items.models import  OrderItem
from payments.models import Payment  # Importez le modèle Payment

def get_order_items(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('dish')
    items_data = [{
        'dish__name': item.dish.name,
        'dish__image': item.dish.image.url if item.dish.image else '',
        'quantity': item.quantity,
        'price': float(item.price),
    } for item in order_items]

    # Récupérer les informations de paiement (si elles existent)
    payments = Payment.objects.filter(order=order)
    payments_data = [{
        'amount': float(payment.amount),
        'payment_method': payment.get_payment_method_display(),
        'created_at': payment.created_at.strftime("%d/%m/%Y %H:%M"),
    } for payment in payments]

    # Récupérer les informations de la commande
    order_data = {
        'id': order.id,
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
        'payments': payments_data,
        'order': order_data,
    })


# Update order

from django.shortcuts import redirect, render, get_object_or_404
from orders.models import Order
from django.contrib import messages

def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status') # get the status from the form.
        current_status = order.status

        if new_status != current_status:
            order.status = new_status
            order.save()
            messages.success(request, 'تم تحديث حالة الطلب بنجاح')
        else:
            messages.info(request, 'لم يتم إجراء أي تغيير على حالة الطلب')

        return redirect('order_list')

    return render(request, 'orders/order_list.html', {'order': order}) # if not a POST request
    
# Delete order
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    messages.success(request,'تم حذف الطلب بنجاح')
    return redirect('order_list')
