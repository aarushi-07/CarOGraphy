from django.urls import path

from myapp import views
from .views import login_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.edit_profile, name='profile'),

]
