from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, Count
from .models import User
import json
import logging
import re

# Configuration du logging pour debug
logger = logging.getLogger(__name__)


def home(request):
    """Page d'accueil avec gestion sécurisée des imports"""
    
    # Calcul sécurisé des totaux
    total_farmers = User.objects.filter(role='farmer').count()
    total_crops = 50  # Valeur par défaut
    
    context = {
        'total_farmers': total_farmers,
        'total_crops': total_crops,
        'recent_tips': [],
        'recent_posts': [],
        'weather_data': None,
        'crops': [],
    }
    return render(request, 'farmconnect_app/home.html', context)


@csrf_protect
@never_cache
def custom_login(request):
    """Vue de connexion personnalisée avec username simple"""
    
    logger.info(f"Login view called with method: {request.method}")
    
    # Rediriger si l'utilisateur est déjà connecté
    if request.user.is_authenticated:
        logger.info("User already authenticated, redirecting to dashboard")
        return redirect('farmconnect_app:dashboard')
    
    # Initialiser le formulaire pour les requêtes GET
    form = AuthenticationForm()
    
    if request.method == 'POST':
        logger.info("Processing POST request for login")
        
        # Récupérer les données du formulaire
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')
        next_url = request.POST.get('next', request.GET.get('next', ''))
        
        logger.info(f"Username: {username}, Password length: {len(password) if password else 0}")
        logger.info(f"Next URL: {next_url}")
        
        # Validation des champs requis
        if not username or not password:
            logger.warning("Missing username or password")
            messages.error(request, _('Veuillez remplir tous les champs requis.'))
            form = AuthenticationForm(data=request.POST)
        else:
            # Créer le formulaire avec les données POST pour la validation
            form = AuthenticationForm(data=request.POST)
            
            # Tentative d'authentification avec username simple
            logger.info(f"Attempting authentication for user: {username}")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                logger.info(f"Authentication successful for user: {user.username}")
                
                if user.is_active:
                    logger.info("User is active, logging in")
                    login(request, user)
                    
                    # Gestion du "Se souvenir de moi"
                    if remember_me:
                        # Session expire dans 2 semaines
                        request.session.set_expiry(1209600)
                        logger.info("Remember me enabled - session set to 2 weeks")
                    else:
                        # Session expire à la fermeture du navigateur
                        request.session.set_expiry(0)
                        logger.info("Remember me disabled - session expires on browser close")
                    
                    # Message de succès
                    user_display_name = user.get_full_name() or user.username
                    messages.success(
                        request, 
                        _('Connexion réussie ! Bienvenue {}').format(user_display_name)
                    )
                    
                    # Déterminer l'URL de redirection
                    if next_url:
                        redirect_to = next_url
                    else:
                        try:
                            redirect_to = reverse('farmconnect_app:dashboard')
                        except:
                            redirect_to = '/dashboard/'
                    
                    logger.info(f"Redirecting authenticated user to: {redirect_to}")
                    
                    # Effectuer la redirection
                    return HttpResponseRedirect(redirect_to)
                else:
                    logger.warning(f"User account {user.username} is inactive")
                    messages.error(
                        request, 
                        _('Votre compte est désactivé. Contactez l\'administrateur.')
                    )
            else:
                logger.warning(f"Authentication failed for username: {username}")
                messages.error(
                    request, 
                    _('Nom d\'utilisateur ou mot de passe incorrect.')
                )
    
    # Préparer le contexte pour le template
    try:
        default_redirect = reverse('farmconnect_app:dashboard')
    except:
        default_redirect = '/dashboard/'
    
    redirect_to = request.GET.get('next', default_redirect)
    
    context = {
        'form': form,
        'redirect_field_name': 'next',
        'redirect_field_value': redirect_to,
    }
    
    logger.info("Rendering login template")
    return render(request, 'registration/login.html', context)

def custom_logout(request):
    """Vue de déconnexion personnalisée"""
    
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, _('Vous avez été déconnecté avec succès. À bientôt {}!').format(user_name))
    
    return redirect('farmconnect_app:home')

def register(request):
    """Vue d'inscription avec username simple"""
    
    print(f"DEBUG: Register view called with method: {request.method}")
    
    if request.user.is_authenticated:
        print("DEBUG: User already authenticated, redirecting to dashboard")
        return redirect('farmconnect_app:dashboard')
        
    if request.method == 'POST':
        print("DEBUG: Processing POST request for registration")
        print(f"DEBUG: POST data keys: {list(request.POST.keys())}")
        
        try:
            data = request.POST
            
            # Debug des données reçues
            username = data.get('username', '').strip()
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
            region = data.get('region', '').strip()
            village = data.get('village', '').strip()
            language = data.get('language', 'fr')
            role = data.get('role', 'farmer')
            
            print(f"DEBUG: Parsed data - Username: {username}, Name: {first_name} {last_name}")
            
            # Validation des champs requis
            required_fields = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': password
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value]
            
            if missing_fields:
                print(f"DEBUG: Missing required fields: {missing_fields}")
                messages.error(request, _('Les champs suivants sont requis: {}').format(', '.join(missing_fields)))
                return render(request, 'registration/register.html')
            
            # Vérification du mot de passe confirmé (si présent)
            if confirm_password and password != confirm_password:
                print("DEBUG: Password confirmation mismatch")
                messages.error(request, _('Les mots de passe ne correspondent pas.'))
                return render(request, 'registration/register.html')
            
            # Validation du nom d'utilisateur
            if len(username) < 3:
                print("DEBUG: Username too short")
                messages.error(request, _('Le nom d\'utilisateur doit contenir au moins 3 caractères.'))
                return render(request, 'registration/register.html')
            
            # Vérification de l'unicité du nom d'utilisateur
            if User.objects.filter(username=username).exists():
                print("DEBUG: Username already exists")
                messages.error(request, _('Ce nom d\'utilisateur est déjà utilisé.'))
                return render(request, 'registration/register.html')
            
            # Vérification de l'unicité de l'email (si fourni)
            if email and User.objects.filter(email=email).exists():
                print("DEBUG: Email already exists")
                messages.error(request, _('Cette adresse email est déjà utilisée.'))
                return render(request, 'registration/register.html')
            
            # Validation du rôle selon vos choix
            valid_roles = ['farmer', 'agent', 'admin']
            if role not in valid_roles:
                role = 'farmer'  # Valeur par défaut
            
            # Validation de la langue selon vos choix
            valid_languages = ['fr', 'wo']
            if language not in valid_languages:
                language = 'fr'  # Valeur par défaut
            
            print(f"DEBUG: Creating user with role: {role}, language: {language}")
            
            # Création de l'utilisateur avec username simple
            print("DEBUG: Creating new user")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                region=region,
                village=village,
                preferred_language=language,
                role=role
            )
            
            print(f"DEBUG: User created successfully with ID: {user.id}")
            
            # Connexion automatique
            login(request, user)
            print("DEBUG: User logged in automatically")
            
            messages.success(request, _('Inscription réussie ! Bienvenue sur FarmConnect Senegal, {}.').format(user.get_full_name()))
            return redirect('farmconnect_app:dashboard')
            
        except Exception as e:
            print(f"DEBUG: Registration error: {str(e)}")
            logger.error(f"Registration error: {str(e)}")
            messages.error(request, _('Erreur lors de l\'inscription: {}').format(str(e)))
    
    print("DEBUG: Rendering registration template")
    return render(request, 'registration/register.html')

@login_required
def dashboard(request):
    """Vue du tableau de bord utilisateur"""
    
    print(f"DEBUG: Dashboard view called for user: {request.user.username}")
    
    user = request.user
    
    # Vérifier si c'est la première connexion
    if not user.last_login or user.created_at == user.last_login:
        messages.info(request, _('Bienvenue sur FarmConnect ! Découvrez toutes nos fonctionnalités.'))
    
    context = {
        'weather_data': None,
        'recent_tips': [],
        'my_posts': [],
        'my_products': [],
        'favorite_crops': [],
        'user': user,
    }
    
    return render(request, 'farmconnect_app/dashboard.html', context)

@login_required
def profile(request):
    """Vue du profil utilisateur - Adaptée au modèle User"""
    
    if request.method == 'POST':
        user = request.user
        
        # Mise à jour des champs de base
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.region = request.POST.get('region', user.region)
        user.village = request.POST.get('village', user.village)
        user.preferred_language = request.POST.get('preferred_language', user.preferred_language)
        
        # Mise à jour de la taille de l'exploitation
        farm_size = request.POST.get('farm_size')
        if farm_size:
            try:
                user.farm_size = float(farm_size)
            except ValueError:
                user.farm_size = None
        else:
            user.farm_size = None
        
        # Mise à jour de la date de naissance
        birth_date = request.POST.get('birth_date')
        if birth_date:
            from datetime import datetime
            try:
                user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                user.birth_date = None
        
        # Gestion de l'upload de photo de profil
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        # Le rôle ne peut être modifié que par un admin
        if request.user.is_superuser or request.user.role == 'admin':
            new_role = request.POST.get('role')
            if new_role in ['farmer', 'agent', 'admin']:
                user.role = new_role
        
        user.save()
        messages.success(request, _('Profil mis à jour avec succès.'))
        return redirect('farmconnect_app:profile')
    
    return render(request, 'farmconnect_app/profile.html')

def about(request):
    """Page à propos"""
    return render(request, 'farmconnect_app/about.html')

def investors(request):
    """Page investisseurs"""
    stats = {
        'total_users': User.objects.count(),
        'active_farmers': User.objects.filter(role='farmer', is_active=True).count(),
        'regions_covered': User.objects.values('region').distinct().count(),
        'crops_supported': 50,  # Valeur par défaut
    }
    
    return render(request, 'farmconnect_app/investors.html', {'stats': stats})

def password_reset_request(request):
    """Vue pour demander une réinitialisation de mot de passe"""
    
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                messages.success(request, _('Un lien de réinitialisation sera envoyé si ce compte existe.'))
            except User.DoesNotExist:
                messages.success(request, _('Un lien de réinitialisation sera envoyé si ce compte existe.'))
        else:
            messages.error(request, _('Veuillez saisir votre nom d\'utilisateur.'))
    
    return render(request, 'registration/password_reset.html')

def debug_view(request):
    """Vue de debug pour tester la configuration"""
    
    context = {
        'user_authenticated': request.user.is_authenticated,
        'user_info': str(request.user) if request.user.is_authenticated else 'Anonymous',
        'session_keys': list(request.session.keys()),
        'post_data': dict(request.POST) if request.method == 'POST' else {},
        'get_data': dict(request.GET),
        'total_users': User.objects.count(),
    }
    
    return render(request, 'farmconnect_app/debug.html', context)


def community(request):
    """Page communauté avec statistiques et informations"""
    
    # Calculer les statistiques de la communauté
    total_farmers = User.objects.filter(role='farmer', is_active=True).count()
    total_regions = User.objects.values('region').distinct().count()
    total_crops = 50  # Valeur par défaut, à remplacer par un modèle Crop si vous en avez
    total_workshops = 100  # Valeur par défaut, à remplacer par un modèle Workshop si vous en avez
    
    # Prochains ateliers (exemple - à adapter selon vos modèles)
    upcoming_workshops = []
    # Si vous avez un modèle Workshop:
    # from datetime import date
    # upcoming_workshops = Workshop.objects.filter(date__gte=date.today()).order_by('date')[:4]
    
    # Témoignages (exemple - à adapter selon vos modèles)
    testimonials = []
    # Si vous avez un modèle Testimonial:
    # testimonials = Testimonial.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    context = {
        'total_farmers': total_farmers,
        'total_regions': total_regions,
        'total_crops': total_crops,
        'total_workshops': total_workshops,
        'upcoming_workshops': upcoming_workshops,
        'testimonials': testimonials,
        # 'community_image': None,  # Ajoutez si vous avez un modèle pour les images
    }
    
    return render(request, 'community/community.html', context)

def about(request):
    """Page à propos de FarmConnect"""
    
    # Statistiques générales
    stats = {
        'total_users': User.objects.count(),
        'active_farmers': User.objects.filter(role='farmer', is_active=True).count(),
        'regions_covered': User.objects.values('region').distinct().count(),
        'years_experience': 2,  # Depuis le lancement de la plateforme
    }
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'farmconnect_app/about.html', context)

def community_view(request):
    return render(request, 'farmconnect_app/community.html')

def investors_view(request):
    return render(request, 'farmconnect_app/investors.html')

def tools_view(request):
    return render(request, 'farmconnect_app/tools.html')


# farmconnect_app/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_test_sms_simple(request):
    """Vue simple pour envoyer un SMS de test"""
    if request.method == 'POST':
        try:
            # Initialiser Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Envoyer le message
            message = client.messages.create(
                body="Test FarmConnect 🌾 - Message envoyé avec succès!",
                from_=settings.TWILIO_PHONE_NUMBER,
                to="+221785423833"  # Votre numéro
            )
            
            # Message de succès
            messages.success(request, f'✅ SMS envoyé avec succès! ID: {message.sid}')
            print(f"SMS envoyé: {message.sid}")  # Pour debug
            
        except TwilioRestException as e:
            messages.error(request, f'❌ Erreur Twilio: {e.msg}')
            print(f"Erreur Twilio: {e}")  # Pour debug
            
        except Exception as e:
            messages.error(request, f'❌ Erreur: {str(e)}')
            print(f"Erreur: {e}")  # Pour debug
        
        # Rediriger vers la même page
        return redirect('farmconnect_app:home')
    
    # GET request - afficher le template
    return render(request, 'farmconnect_app/home.html')