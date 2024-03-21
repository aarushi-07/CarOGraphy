from django.urls import path
from myapp import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
<<<<<<< HEAD
    path('profile/', views.edit_profile, name='profile'),
    # path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('user-guide/', views.user_guide, name='user_guide'),
    # reset password feature urls 
    # done by Arish 
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('user-history/', views.user_history_view, name='user_history'),


=======
    path('profile/', views.update_profile, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('user-guide/', views.user_guide, name='user_guide')
>>>>>>> 6d637923cd5fb747f963c1ec262add692385578b
]
