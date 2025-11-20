from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'farmconnect_app'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),

    # Authentification
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),

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

    # Pages utilisateur (protected)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # Pages statiques
    path('about/', views.about, name='about'),
    path('investors/', views.investors, name='investors'),
    path('community/', views.community, name='community'),

    # Marketplace (ancien Tools)
    path('marketplace/', views.marketplace_view, name='marketplace'),
    path('tools/', views.marketplace_view, name='tools'),  # Redirection pour compatibilité

    # Orders
    path('place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Admin Dashboard (custom)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/prices/', views.admin_prices, name='admin_prices'),
    path('admin-dashboard/events/', views.admin_events, name='admin_events'),
    path('admin-dashboard/products/', views.admin_products, name='admin_products'),
    path('admin-dashboard/advice/', views.admin_advice, name='admin_advice'),
    path('admin-dashboard/orders/', views.admin_orders, name='admin_orders'),
]
