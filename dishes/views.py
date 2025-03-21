from django.shortcuts import render, redirect
from .models import *
from categories.models import Category
# paginations
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(dishes, 5)  # Show 5 dishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dishes/index.html', {'dishes': page_obj,'page_obj': page_obj, 'categories': categories})
    # return render(request, 'dishes/index.html', {'dishes': dishes, 'categories': categories})
    # return render(request, 'dishes/index.html')
# search
import json
from django.http import JsonResponse, HttpResponse

# def search(request):
#     if request.method == 'GET':
#         query = request.GET.get('query')
#         dishes = Dish.objects.filter(name__icontains=query) | Dish.objects.filter(
#                 category__icontains=query) 
#         data = dishes.values()
#         return JsonResponse(list(data), safe=False)
def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        dishes = Dish.objects.filter(name__icontains=query) 
        categories = Category.objects.all()
        if not dishes:
            messages.error(request, 'لا يوجد نتائج')
            return redirect('dishes')
        paginator = Paginator(dishes, 5)  # Show 5 dishes per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        return render(request, 'dishes/index.html', {'dishes': page_obj,'page_obj': page_obj, 'categories': categories})
        
# add
from django.contrib import messages


def add_dishe(request):
    categories = Category.objects.all() 
    context = {'categories': categories, 'values': request.POST}
    
    if request.method == 'GET':
        return render(request, 'dishes/add_dishe.html', context)
    
    if request.method == 'POST':
        price = request.POST['price']
        name = request.POST['name']
        date = request.POST['created_at']
        category_name = request.POST['category']  # Nom de la catégorie sélectionnée
        image = request.FILES.get('image')  # Utilisez .get() pour éviter KeyError si le champ est vide
        print(request.FILES)  # Vérifiez si le fichier image est bien reçu

        # Validation des champs obligatoires
        if not price or not name or not date or not category_name or not image:
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'dishes/add_dishe.html', context)

        # Récupérer l'instance de Category correspondante
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Catégorie invalide')
            return render(request, 'dishes/add_dishe.html', context)

        # Créer l'objet Dish
        Dish.objects.create(
            price=price,
            name=name,
            created_at=date,
            category=category,  # Assigner l'instance de Category
            image=image
        )

        messages.success(request, 'Plat ajouté avec succès')
        return redirect('dishes')

def update_dish(request,id):
    dish = Dish.objects.get(pk=id)
    categories = Category.objects.all() 
    context = {'dish': dish,'categories': categories, 'values': dish}
    
    if request.method == 'GET':
        return render(request, 'dishes/edit_dishe.html', context)
    
    if request.method == 'POST':
        price = request.POST['price']
        name = request.POST['name']
        date = request.POST['created_at']
        category_name = request.POST['category']  # Nom de la catégorie sélectionnée
        image = dish.image if request.FILES.get('image') is None else request.FILES.get('image')   # Utilisez .get() pour éviter KeyError si le champ est vide
        print(request.FILES)  # Vérifiez si le fichier image est bien reçu

        # Validation des champs obligatoires
        print('Name: ',name ,'price: ',price,'category: ',category_name,'image: ',image,'date:',date)
        if not price or not name or not date or not category_name or not image:
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'dishes/edit_dishe.html', context)

        # Récupérer l'instance de Category correspondante
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Catégorie invalide')
            return render(request, 'dishes/edit_dishe.html', context)

        # Créer l'objet Dish
        
        dish.price=price
        dish.name=name
        dish.created_at=date
        dish.category=category  # Assigner l'instance de Category
        dish.image=image
        dish.save()

        messages.success(request, 'Plat modifé avec succès')
        return redirect('dishes')

# delete

def delete_dish(request,id):
    dish = Dish.objects.get(pk=id)
    dish.delete()
    messages.success(request, 'Plat supprimé avec succès')
    return redirect('dishes')

# export as excel

from django.http import HttpResponse
import pandas as pd

def export_to_excel(request):
    dishes = Dish.objects.all()
    df = pd.DataFrame(list(dishes.values('id', 'name', 'price',  'category__name')))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=dishes.xlsx'
    df.to_excel(response, index=False)
    messages.success(request, 'تمت لتحميل')
    return response

# to pdf

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def export_to_pdf(request):
    dishes = Dish.objects.all()
    print('Dish_name: ',dishes[0].name)
    template = get_template('dishes/pdf_template.html')
    html = template.render({'dishes': dishes})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dishes.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response