from django.shortcuts import render, redirect
from categories.models import Category
from dishes.models import Dish
from tables.models import Table
# paginations
from django.core.paginator import Paginator
# datetime
from datetime import datetime
from django.contrib import messages

def index(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 6)  # Show 5 dishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    selected_category_id = request.GET.get('category_id')
    dishes = Dish.objects.filter(category_id=selected_category_id) if selected_category_id else Dish.objects.none()
    tables = Table.objects.filter(status='متاحة')

    # Gérer les plats sélectionnés dans la session
    if 'order_dishes' not in request.session:
        request.session['order_dishes'] = []

    # Ajouter un plat à la commande
    selected_dish_id = request.GET.get('dish_id')
    if selected_dish_id:
        dish = Dish.objects.get(id=selected_dish_id)
        if selected_dish_id not in [d['id'] for d in request.session['order_dishes']]:
            request.session['order_dishes'].append({
                'id': dish.id,
                'name': dish.name,
                'image': dish.image.url,
                'price': float(dish.price),
                'quantity': 1,
            })
            request.session.modified = True

    # Récupérer les plats de la session
    order_dishes = []
    for item in request.session['order_dishes']:
        dish = Dish.objects.get(id=item['id'])
        order_dishes.append({
            'dish': dish,
            'quantity': item['quantity'],
        })
    current_date = datetime.now().strftime('%Y-%m-%d : %Hh:%Mmin')
    print('Current Date:', current_date)
    return render(request, 'point_of_sale/index.html', {
        'categories': page_obj,
        'dishes': dishes,
        'tables': tables,
        'selected_category_id': selected_category_id,
        'order_dishes': order_dishes,
        'current_date': current_date,
    })

def remove_dish(request, dish_id):
    if 'order_dishes' in request.session:
        request.session['order_dishes'] = [d for d in request.session['order_dishes'] if d['id'] != dish_id]
        request.session.modified = True
    return redirect('point_of_sale')

def clear_order(request):
    if 'order_dishes' in request.session:
        del request.session['order_dishes']
    return redirect('point_of_sale')

def update_quantity(request, dish_id, action):
    if 'order_dishes' in request.session:
        for item in request.session['order_dishes']:
            if item['id'] == dish_id:
                if action == 'increase':
                    item['quantity'] += 1
                elif action == 'decrease' and item['quantity'] > 1:
                    item['quantity'] -= 1
                request.session.modified = True
                break
    return redirect('point_of_sale')


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order
from order_items.models import OrderItem
from dishes.models import Dish
from tables.models import Table
from django.contrib import messages
from payments.models import Payment  # Import the Payment model

@login_required
def create_order(request):
    if request.method == 'POST':
        if 'order_dishes' in request.session and request.session['order_dishes']:
            user = request.user
            order_type = request.POST.get('order_type')
            payment_method = request.POST.get('payment_method')  # Get the payment method

            # Calculate the total price
            total_price = sum(item['price'] * item['quantity'] for item in request.session['order_dishes'])

            # Create the order
            if order_type == 'dine_in':
                table_id = request.POST.get('table')
                table = Table.objects.get(id=table_id) if table_id else None
                order = Order.objects.create(
                    user=user,
                    table=table,
                    total_price=total_price,
                    order_type=order_type,
                    status='قيد التنفيذ',
                )
                # change status of the table
                if table:
                    table.status = 'محجوزة'
                    table.save()
                    
            elif order_type == 'take_out':
                pickup_time = request.POST.get('pickup_time')
                order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    order_type=order_type,
                    pickup_time=pickup_time,
                    status='قيد التنفيذ',
                )
            elif order_type == 'delivery':
                delivery_address = request.POST.get('delivery_address')
                phone_number = request.POST.get('phone_number')
                order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    order_type=order_type,
                    delivery_address=delivery_address,
                    phone_number=phone_number,
                    status='قيد التنفيذ',
                )
            else:
                messages.error(request, 'نوع الطلب غير صحيح')
                return redirect('point_of_sale')

            # Add dishes to the order
            for item in request.session['order_dishes']:
                dish = Dish.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    dish=dish,
                    quantity=item['quantity'],
                    price=item['price'],
                )

            # Create a payment for the order
            Payment.objects.create(
                order=order,
                amount=total_price,
                payment_method=payment_method,
            )

            # Clear the session after creating the order
            del request.session['order_dishes']
            
            messages.success(request, 'تم اضافة الطلب بنجاح')
            return redirect('order_list')

    messages.error(request, 'لا توجد وجبات في الطلب')
    return redirect('point_of_sale')