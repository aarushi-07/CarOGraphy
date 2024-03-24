from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from myapp.forms import  CreateUserForm, ProfileForm, LoginForm
from myapp.models import Profile, ChatWindow, ChatMessage, CarService, ServiceForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from myapp.forms import ProfileForm,FeedbackForm, UserForm, PaymentForm
from myapp.forms import ProfileForm,FeedbackForm, UserForm
from myapp.forms import ProfileForm
from myapp.models import ChatWindow, Profile, ChatMessage
from myapp.forms import CreateUserForm, ProfileForm, LoginForm
from myapp.models import Profile
from django.contrib.auth.decorators import login_required


def authenticate_user(email=None, password=None):
    try:
        user = Profile.objects.get(email=email)
        print(user)
        if user.check_password(password):
            print(user)
            return user
        else:
            return None
    except Profile.DoesNotExist:
        return None  # Return None if the user does not exist

def login_view(request):
    invalid_credentials = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate_user(email, password)
            if user is not None:
                login(request, user)
                return redirect('myapp:landing')  # Redirect to the appropriate URL
            else:
                invalid_credentials = True
                print(invalid_credentials)
                return render(request, 'myapp/login.html', {'form': form, 'invalid_credentials': invalid_credentials})
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form, 'invalid_credentials' : invalid_credentials})

@login_required
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
            return redirect('myapp:login')
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


@login_required(login_url='login')
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
        # messages.success(request, 'Your message has been sent!')
        
        # Redirect to the same page after POST
        return redirect('myapp:contact-us')

    return render(request, 'myapp/contact_us.html')


def logout_view(request):
    return redirect('login')


def chat_application(request, user_id=None):
    if user_id:
        # Assuming the logged-in user is the first person in the thread
        user1 = request.user
        user2 = get_object_or_404(User, id=user_id)
        thread, created = Profile.objects.get_or_create(
            first_person=user1,
            second_person=user2,
        )
        messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
        context = {
            'thread': thread,
            'messages': messages,
        }
        return render(request, 'myapp/message.html', context)
    else:
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'myapp/message.html', context)


@login_required
def chat(request, user):
    # Assuming Profile is related to the custom User model
    if user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        last_active_userchat_id = request.session.get('last_active_userchat_id')
        userchats = ChatWindow.objects.filter(Q(user1=user_profile) | Q(user2=user_profile)).prefetch_related(
            'chatmessage_userchat').order_by('timestamp').distinct()

        context = {
            'userchats': userchats,
            'last_active_userchat_id': last_active_userchat_id
        }

        return render(request, 'myapp/message.html', context)


# def chat(request):
#     return render(request, 'myapp/chat.html')


# def garage_user_history(request):
#     clicked_garages_ids = request.session.get('clicked_garages', [])
#     clicked_garages = Cargaragedata.objects.filter(id__in=clicked_garages_ids)

#     return render(request, 'clicked_garages.html', {'clicked_garages': clicked_garages})

def garage_user_history(request):
    # Simulate a list of clicked garages with hard-coded data
    clicked_garages = [
        {'name': 'Garage A', 'rating': 4.5, 'address': '123 Main St', 'contact_number': '555-1234', 'website': 'http://example.com'},
        {'name': 'Garage B', 'rating': 4.2, 'address': '456 Elm St', 'contact_number': '555-5678', 'website': 'http://example.org'},
        # Add more simulated garages as needed
    ]

    return render(request, 'myapp/garage_user_history.html', {'clicked_garages': clicked_garages})

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user.profile  # Assuming request.user is authenticated and has a profile
            feedback.save()
            return redirect('feedback_success')  # Redirect to a success page after feedback submission
    else:
        form = FeedbackForm()
    return render(request, 'myapp/feedback.html', {'form': form})


def chat_application(request, user_id=None):
    if user_id:
        # Assuming the logged-in user is the first person in the thread
        user1 = request.user
        user2 = get_object_or_404(User, id=user_id)
        thread, created = Thread.objects.get_or_create(
            first_person=user1,
            second_person=user2,
        )
        messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
        context = {
            'thread': thread,
            'messages': messages,
        }
        return render(request, 'myapp/message.html', context)
    else:
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'myapp/message.html', context)

class Thread:
    pass

# @login_required
def messages(request):

    user_profile = Profile.objects.get(user=request.user)
    last_active_userchat_id = request.session.get('last_active_userchat_id')
    userchats = ChatWindow.objects.filter(Q(user1=user_profile) | Q(user2=user_profile)).prefetch_related('chatmessage_userchat').order_by('timestamp').distinct()

    context = {
        'userchats': userchats,
        'last_active_userchat_id': last_active_userchat_id
    }

    return render(request, 'myapp/message.html', context)

def home_view(request):
    services = CarService.objects.all()[0:3]
    return render(request, 'myapp/home.html', {'services': services})

def services(request):
    return render(request, 'myapp/services.html')

def services_view(request):
    services = CarService.objects.all()
    return render(request, 'myapp/services.html', {'services': services})

def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Saves form data to the database
            return redirect('myapp:payment')  # Redirect to a success page or another view
    else:
        form = UserForm()
    return render(request, 'myapp/user_form.html', {'form': form})

def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment (validate card number, CVV, etc.)
            # If payment is successful, redirect to payment success pop-up window
            return render(request, 'myapp/payment_success.html')
    else:
        form = PaymentForm()
    return render(request, 'myapp/payment_form.html', {'form': form})
# def garage_user_history(request):
#     clicked_garages_ids = request.session.get('clicked_garages', [])
#     clicked_garages = Cargaragedata.objects.filter(id__in=clicked_garages_ids)

#     return render(request, 'clicked_garages.html', {'clicked_garages': clicked_garages})

def garage_user_history(request):
    # Simulate a list of clicked garages with hard-coded data
    clicked_garages = [
        {'name': 'Garage A', 'rating': 4.5, 'address': '123 Main St', 'contact_number': '555-1234', 'website': 'http://example.com'},
        {'name': 'Garage B', 'rating': 4.2, 'address': '456 Elm St', 'contact_number': '555-5678', 'website': 'http://example.org'},
        # Add more simulated garages as needed
    ]

    return render(request, 'myapp/garage_user_history.html', {'clicked_garages': clicked_garages})
