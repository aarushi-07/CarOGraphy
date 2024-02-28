from django.urls import path
from myapp import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.edit_profile, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('user-guide/', views.user_guide, name='user_guide')
]
