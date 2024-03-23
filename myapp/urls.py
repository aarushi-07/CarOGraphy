from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.update_profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'), name='password_reset_complete'),
    path('user-guide/', views.user_guide, name='user_guide'),
    path('messages/', views.chat,name='chat'),
    path('contact-us/', views.contact_us, name='contact-us'),
    
]
