from django.shortcuts import render, redirect
from .models import *
from dishes.models import Dish
import json
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
# Create your views here.
from django.db.models import Count

from django.core.paginator import Paginator
# Create your views here.
def index(request):
    categories = Category.objects.annotate(dish_count=Count('dish'))
    dishes = Dish.objects.all()
    paginator = Paginator(categories, 5)  # Show 5 dishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categories/index.html', {'dishes': dishes,'page_obj': page_obj, 'categories': page_obj})

# search
def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        dishes = Dish.objects.all()
        categories = Category.objects.filter(name__icontains=query) 
        if not categories:
            messages.error(request, 'لا يوجد نتائج')
            return redirect('categories')
        paginator = Paginator(categories, 5)  # Show 5 dishes per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        return render(request, 'categories/index.html', {'dishes': dishes,'page_obj': page_obj, 'categories': page_obj})

# add


def add_category(request):
    categories = Category.objects.all() 
    context = {'categories': categories, 'values': request.POST}
    
    if request.method == 'GET':
        return render(request, 'categories/add_category.html', context)
    
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['created_at']
        image = request.FILES.get('image')  # Utilisez .get() pour éviter KeyError si le champ est vide
        print(request.FILES)  # Vérifiez si le fichier image est bien reçu

        # Validation des champs obligatoires
        if  not name or not date or not image:
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'categories/add_category.html', context)

        # Créer l'objet category
        Category.objects.create(
            name=name,
            created_at=date,
            image=image
        )

        messages.success(request, 'categorie ajouté avec succès')
        return redirect('categories')

def update_category(request,id):
    category = Category.objects.get(pk=id)
    context = {'category': category, 'values': category}
    
    if request.method == 'GET':
        return render(request, 'categories/edit_category.html', context)
    
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['created_at']
        image = category.image if request.FILES.get('image') is None else request.FILES.get('image')   # Utilisez .get() pour éviter KeyError si le champ est vide
        print(request.FILES)  # Vérifiez si le fichier image est bien reçu

        # Validation des champs obligatoires
        if not name or not date or not image:
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'categories/edit_category.html', context)



        # Créer l'objet category
        category.name=name
        category.created_at=date
        category.image=image
        category.save()

        messages.success(request, 'categorie modifé avec succès')
        return redirect('categories')

# delete

def delete_category(request,id):
    category = Category.objects.get(pk=id)
    category.delete()
    messages.success(request, 'categorie supprimé avec succès')
    return redirect('categories')
