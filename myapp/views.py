from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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


def home_view(request):
    return render(request, 'home.html')


def edit_profile(request):
    return render(request, 'profile.html')
