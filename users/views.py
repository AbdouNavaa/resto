from django.shortcuts import render,redirect
from .models import User
from django.core.paginator import Paginator

# Create your views here.
# index
def index(request):
    users = User.objects.all()
    paginator = Paginator(users, 5)  # Show 5 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/index.html', {'page_obj': page_obj, 'users': page_obj})

# create
def create(request):
    if request.method == 'GET':
        return render(request, 'users/add_user.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        image = request.FILES.get('image')  # Utilisez .get() pour éviter KeyError si le champ est vide
        print(request.FILES)  # Vérifiez si le fichier image est bien reçu
        User.objects.create(username=username, email=email, password=password,image=image)
        return redirect('users')

# update
def update( request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'users/edit_user.html', {'user': user,'values': user})
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        image = user.image if request.FILES.get('image') is None else request.FILES.get('image')   # Utilisez .get() pour éviter KeyError si le champ est vide
        print(request.FILES)  # Vérifiez si le fichier image est bien reçu
        user.username = username
        user.email = email
        user.password = password
        user.image = image
        user.save()
        return redirect('users')

# delete

def delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('users')

# LOGIN
from django.contrib import auth
from django.contrib import messages

def login(request):
    
    if request.method == 'GET':
        return render(request, 'users/login.html',{'values':request.POST})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username, password=password).first()
        if user:
            auth.login(request, user)  # Authenticate the user
            return redirect('users')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html', {'error': 'Invalid credentials','values': request.POST})
        