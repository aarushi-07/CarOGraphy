from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import CarUser


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid email or password'})
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'User with this email already exists'})

        user = User.objects.create_user(username=username,email=email, password=password)
        user.save()

        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect('login')  
    return render(request, 'register.html')


def home_view(request):
    return render(request, 'home.html')

def edit_profile(request):
    return render(request, 'profile.html')
