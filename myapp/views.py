from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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

<<<<<<< HEAD
def landing(request):
    return render(request, 'myapp/landing.html')
=======


# def user_history_view(request):
#     last_login = request.session.get('last_login')
#     if last_login:
#         last_login = parse_datetime(last_login)
#         last_login_str = last_login.strftime("%Y-%m-%d %H:%M:%S")
#     else:
#         last_login_str = "Never"

#     visits = request.COOKIES.get('visits', '0')
    
#     return HttpResponse(f"Last Login: {last_login_str}, Number of Visits: {visits}")


def contact_us(request):
    return render(request, 'contact_us.html')



# def user_history_view(request):
#     # Retrieve the number of visits and visit history from session
#     visits = request.session.get('visits', 0)
#     visit_history = request.session.get('visit_history', [])

#     # Format the timestamps for display
#     formatted_visit_history = [parse_datetime(ts).strftime("%Y-%m-%d %H:%M:%S") for ts in visit_history]

#     history_str = "<br>".join(formatted_visit_history)

#     return HttpResponse(f"Total Visits: {visits}<br>Visit History:<br>{history_str}")


def user_history_view(request):
    # Retrieve the number of visits and visit history from the session
    visits = request.session.get('visits', 0)
    visit_history = request.session.get('visit_history', [])
    
    # Format the timestamps for display
    formatted_visit_history = [
        parse_datetime(ts).strftime("%Y-%m-%d %H:%M:%S") for ts in visit_history
    ]

    # Pass the formatted visit history to the template
    context = {
        'visits': visits,
        'visit_history': formatted_visit_history
    }

    # Render the template with context
    return render(request, 'user_history.html', context)

>>>>>>> 35650d3 (contact us and user history view intial)
