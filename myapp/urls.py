from django.urls import path
from myapp import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.landing, name='landing'),
    # path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.update_profile, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('user-guide/', views.user_guide, name='user_guide'),
    # path('chat/', views.chat,name='chat'),
    path('logout/', views.logout_view,name='logout')
]
