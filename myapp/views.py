from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from myapp.forms import  CreateUserForm, ProfileForm, LoginForm
from myapp.models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from myapp.forms import ProfileForm

def authenticate_user(email=None, password=None):
    try:
        # Try to fetch the user by username from your custom user model
        user = Profile.objects.get(email=email)
        print(user)
        # Check if the provided password matches the user's password
        if user.check_password(password):
            print(user)  # Return the user object if authentication succeeds
            return user
        else:
            return None  # Return None if the password is incorrect
    except Profile.DoesNotExist:
        return None  # Return None if the user does not exist

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate_user(email, password)
            print(user)
            if user is not None:
                # If authentication succeeds, log in the user and redirect
                login(request, user)
                return redirect('landing')  # Redirect to the appropriate URL
            else:
                # If authentication fails, render the login form with an error message
                error_message = 'Invalid username or password'
    else:
        form = LoginForm()
    error_message = 'Invalid username or password'
    return render(request, 'myapp/login.html', {'form': form,'error_message': error_message})



def logout_view(request):
    return redirect('login')

def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            print(user)
            return redirect('login')
    else:
        form = CreateUserForm()

    # If the form is invalid or it's a GET request, include the form in the context
    context = {'form': form}
    return render(request, 'myapp/register.html', context)




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
@login_required
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
@login_required
def landing(request):
    return render(request, 'myapp/landing.html')

def chat(request):
    return render(request, 'myapp/chat.html')


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