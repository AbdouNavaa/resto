from django.shortcuts import render, redirect
from .models import Coupon
from django.core.paginator import Paginator

# Create your views here.
# index
def index(request):
    coupons = Coupon.objects.all()
    # paginations
    paginator = Paginator(coupons, 5)  # Show 5 dishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'coupons/index.html', {'coupons': page_obj, 'page_obj': page_obj})

# create
def create(request):
    context = { 'values': request.POST}
    
    if request.method == 'GET':
        return render(request, 'coupons/add_coupon.html', context)
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        status = request.POST['status']
        Coupon.objects.create(status=status, code=code, discount_percentage=discount)
        return redirect('coupons')
    return render(request, 'coupons/add_coupon.html',context)

# update
def update(request, id):
    coupon = Coupon.objects.get(pk=id)
    print(coupon)
    context = {'coupon': coupon, 'values': coupon}
    if request.method == 'GET':
        return render(request, 'coupons/edit_coupon.html', context)
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        status = request.POST['status']
        coupon.code = code
        coupon.discount_percentage = discount
        coupon.status = status
        coupon.save()
        return redirect('coupons')
    return render(request, 'coupons/edit_coupon.html', context)

# delete
def delete(request, id):
    coupon = Coupon.objects.get(pk=id)
    coupon.delete()
    return redirect('coupons')
