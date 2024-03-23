from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from myapp.forms import ProfileForm


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
            return render(request, 'myapp/login.html', {'error_message': 'Invalid email or password'})
    else:
        return render(request, 'myapp/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'myapp/register.html', {'error_message': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            return render(request, 'myapp/register.html', {'error_message': 'User with this email already exists'})

        user = User.objects.create_user(username=username,email=email, password=password)
        user.save()

        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect('login')
    return render(request, 'myapp/register.html')


def home_view(request):
    return render(request, 'myapp/home.html')


def update_profile(request):
    profile = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home.html')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'myapp/profile.html', {'form': form})

def forgot_password(request):
    return render(request, 'myapp/forgot_password.html')

def user_guide(request):
    content = {
        'title': 'Carography User Guide',
        'sections': [
            {
                'title': 'Introduction',
                'content': 'Welcome to the Carography User Guide!'
            },
        ]
    }
    return render(request, 'myapp/UserGuide.html', content)

def landing(request):
    return render(request, 'myapp/landing.html')



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        
        send_mail(
            f"Message from {name} - {subject}",
            message,
            'internetapplicationsclass@gmail.com',
            [email],  # Replace with your email
            fail_silently=False,
        )

        # Show a success message
        messages.success(request, 'Your message has been sent!')
        
        # Redirect to the same page after POST
        return redirect('contact-us')

    return render(request, 'myapp/contact_us.html')