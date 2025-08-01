# farmconnect_app/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'farmconnect_app'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),  # Alternative URL
    
    # Authentification
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Pages utilisateur
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Pages statiques
    path('about/', views.about, name='about'),
    path('investors/', views.investors, name='investors'),
    path('tools/', views.tools_view, name='tools'),
    
    # Community
    path('community/', views.community_view, name='community'),
    
    # SMS et API
    
    path('test-sms-simple/', views.send_test_sms_simple, name='send_test_sms_simple'),
    
    # Réinitialisation de mot de passe
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]