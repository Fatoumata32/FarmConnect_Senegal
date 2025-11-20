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
from .security import rate_limit_login, rate_limit_api
import json
import logging
import re

# Configuration du logging pour debug
logger = logging.getLogger(__name__)


def home(request):
    """Page d'accueil avec données réelles"""
    from crops.models import Crop, CropTip
    from community.models import ForumPost
    from advice.models import CropAdvice

    # Calcul des totaux depuis la base de données
    total_farmers = User.objects.filter(role='farmer', is_active=True).count()
    total_crops = Crop.objects.filter(is_active=True).count()

    # Récupérer les données récentes
    recent_tips = CropTip.objects.select_related('crop', 'created_by').order_by('-created_at')[:5]
    recent_posts = ForumPost.objects.filter(is_active=True).select_related('author').order_by('-created_at')[:5]
    crops = Crop.objects.filter(is_active=True).order_by('name_fr')[:8]

    # Récupérer 6 conseils de cultures aléatoires pour la page d'accueil
    crop_advice_previews = CropAdvice.objects.filter(is_active=True).select_related('crop').order_by('?')[:6]

    context = {
        'total_farmers': total_farmers,
        'total_crops': total_crops,
        'recent_tips': recent_tips,
        'recent_posts': recent_posts,
        'weather_data': None,
        'crops': crops,
        'crop_advice_previews': crop_advice_previews,
    }
    return render(request, 'farmconnect_app/home.html', context)


@csrf_protect
@never_cache
@rate_limit_login(requests_per_minute=5)
def custom_login(request):
    """Vue de connexion personnalisée avec username simple"""
    
    logger.info(f"Login view called with method: {request.method}")
    
    # Rediriger si l'utilisateur est déjà connecté
    if request.user.is_authenticated:
        # Rediriger admin vers admin dashboard, autres vers dashboard normal
        if request.user.is_superuser or request.user.role == 'admin':
            logger.info("Admin user already authenticated, redirecting to admin dashboard")
            return redirect('farmconnect_app:admin_dashboard')
        else:
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
                        # Rediriger admin vers admin dashboard
                        if user.is_superuser or user.role == 'admin':
                            try:
                                redirect_to = reverse('farmconnect_app:admin_dashboard')
                            except:
                                redirect_to = '/admin-dashboard/'
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
    """Page investisseurs avec statistiques réelles"""
    from crops.models import Crop

    stats = {
        'total_users': User.objects.count(),
        'active_farmers': User.objects.filter(role='farmer', is_active=True).count(),
        'regions_covered': User.objects.values('region').exclude(region='').distinct().count(),
        'crops_supported': Crop.objects.filter(is_active=True).count(),
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
    """Page communauté avec statistiques, prix du marché et événements"""
    from crops.models import Crop
    from community.models import ForumPost, MarketPrice, Event
    from django.db.models import Avg, Max, Min
    from datetime import date, timedelta

    # Get latest market prices (one per crop, most recent)
    latest_prices = []
    crops_with_prices = MarketPrice.objects.values_list('crop_name', flat=True).distinct()

    for crop in crops_with_prices:
        latest_price = MarketPrice.objects.filter(crop_name=crop).order_by('-date').first()
        if latest_price:
            latest_prices.append(latest_price)

    # Get regional variations for display
    regional_data = []
    for crop in list(crops_with_prices)[:5]:  # Top 5 crops
        crop_prices = MarketPrice.objects.filter(
            crop_name=crop,
            date__gte=date.today() - timedelta(days=7)
        )
        if crop_prices.exists():
            regional_data.append({
                'crop': crop,
                'avg_price': round(crop_prices.aggregate(Avg('price_per_kg'))['price_per_kg__avg'], 2),
                'max_price': round(crop_prices.aggregate(Max('price_per_kg'))['price_per_kg__max'], 2),
                'min_price': round(crop_prices.aggregate(Min('price_per_kg'))['price_per_kg__min'], 2),
                'regions_count': crop_prices.values('region').distinct().count()
            })

    # Calculer les statistiques de la communauté
    total_farmers = User.objects.filter(role='farmer', is_active=True).count()
    total_regions = User.objects.values('region').exclude(region='').distinct().count()
    total_crops = Crop.objects.filter(is_active=True).count()
    total_posts = ForumPost.objects.filter(is_active=True).count()

    # Posts récents
    recent_posts = ForumPost.objects.filter(is_active=True).select_related('author').order_by('-created_at')[:5]

    # Upcoming events
    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=date.today()
    ).order_by('date', 'start_time')[:5]

    # Total workshops/events
    total_workshops = Event.objects.filter(is_active=True).count()

    context = {
        'latest_prices': latest_prices[:10],  # Top 10 crops
        'regional_data': regional_data,
        'total_farmers': total_farmers,
        'total_regions': total_regions,
        'total_crops': total_crops,
        'total_workshops': total_workshops,
        'total_posts': total_posts,
        'upcoming_workshops': [],
        'testimonials': [],
        'recent_posts': recent_posts,
        'upcoming_events': upcoming_events,
    }

    return render(request, 'farmconnect_app/community.html', context)

def community_view(request):
    return render(request, 'farmconnect_app/community.html')

def investors_view(request):
    return render(request, 'farmconnect_app/investors.html')

def tools_view(request):
    """Ancienne vue - redirige vers marketplace"""
    return render(request, 'farmconnect_app/marketplace.html')

def marketplace_view(request):
    """
    Vue Marketplace/Tools - Outils agricoles avec paiements échelonnés
    """
    from marketplace.models import Product

    # Charger les produits depuis la base de données
    products = Product.objects.filter(is_available=True).order_by('-created_at')

    # Obtenir les catégories uniques
    categories = Product.objects.filter(is_available=True).values_list('category', flat=True).distinct()

    context = {
        'page_title': 'Outils Agricoles',
        'products': products,
        'categories': categories,
    }
    return render(request, 'farmconnect_app/tools.html', context)


# ============================================
# ADMIN DASHBOARD VIEWS
# ============================================

def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('farmconnect_app:login')
        if not (request.user.is_superuser or request.user.role == 'admin'):
            messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
            return redirect('farmconnect_app:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Dashboard principal de l'admin"""
    from community.models import MarketPrice, Event
    from marketplace.models import Product, ToolOrder
    from advice.models import CropAdvice

    context = {
        'total_farmers': User.objects.filter(role='farmer', is_active=True).count(),
        'total_products': Product.objects.filter(is_available=True).count(),
        'total_events': Event.objects.filter(is_active=True).count(),
        'total_prices': MarketPrice.objects.count(),
        'total_advice': CropAdvice.objects.filter(is_active=True).count(),
        'total_orders': ToolOrder.objects.count(),
        'pending_orders': ToolOrder.objects.filter(status='pending').count(),
        'recent_prices': MarketPrice.objects.all().order_by('-date')[:5],
        'upcoming_events': Event.objects.filter(is_active=True).order_by('date')[:5],
        'recent_products': Product.objects.all().order_by('-created_at')[:5],
        'recent_orders': ToolOrder.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@admin_required
def admin_prices(request):
    """Gestion des prix du marché"""
    from community.models import MarketPrice

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            MarketPrice.objects.create(
                crop_name=request.POST.get('crop_name'),
                region=request.POST.get('region'),
                price_per_kg=request.POST.get('price_per_kg'),
                trend=request.POST.get('trend', 'stable'),
                percentage_change=request.POST.get('percentage_change', 0)
            )
            messages.success(request, "Prix ajouté avec succès!")

        elif action == 'update':
            price_id = request.POST.get('price_id')
            price = MarketPrice.objects.get(id=price_id)
            price.price_per_kg = request.POST.get('price_per_kg')
            price.trend = request.POST.get('trend')
            price.percentage_change = request.POST.get('percentage_change', 0)
            price.save()
            messages.success(request, "Prix mis à jour avec succès!")

        elif action == 'delete':
            price_id = request.POST.get('price_id')
            MarketPrice.objects.filter(id=price_id).delete()
            messages.success(request, "Prix supprimé avec succès!")

        return redirect('farmconnect_app:admin_prices')

    prices = MarketPrice.objects.all().order_by('-date', 'crop_name')
    regions = MarketPrice.REGION_CHOICES

    return render(request, 'admin_dashboard/prices.html', {
        'prices': prices,
        'regions': regions,
    })


@admin_required
def admin_events(request):
    """Gestion des événements"""
    from community.models import Event

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            Event.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                event_type=request.POST.get('event_type'),
                date=request.POST.get('date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time') or None,
                location=request.POST.get('location'),
                region=request.POST.get('region'),
                organizer=request.POST.get('organizer'),
                contact_phone=request.POST.get('contact_phone', ''),
                contact_email=request.POST.get('contact_email', ''),
                is_free=request.POST.get('is_free') == 'on',
                created_by=request.user
            )
            messages.success(request, "Événement ajouté avec succès!")

        elif action == 'update':
            event_id = request.POST.get('event_id')
            event = Event.objects.get(id=event_id)
            event.title = request.POST.get('title')
            event.description = request.POST.get('description')
            event.event_type = request.POST.get('event_type')
            event.date = request.POST.get('date')
            event.start_time = request.POST.get('start_time')
            event.end_time = request.POST.get('end_time') or None
            event.location = request.POST.get('location')
            event.region = request.POST.get('region')
            event.organizer = request.POST.get('organizer')
            event.is_active = request.POST.get('is_active') == 'on'
            event.save()
            messages.success(request, "Événement mis à jour avec succès!")

        elif action == 'delete':
            event_id = request.POST.get('event_id')
            Event.objects.filter(id=event_id).delete()
            messages.success(request, "Événement supprimé avec succès!")

        return redirect('farmconnect_app:admin_events')

    events = Event.objects.all().order_by('date')

    return render(request, 'admin_dashboard/events.html', {
        'events': events,
        'event_types': Event.EVENT_TYPE_CHOICES,
        'regions': Event.REGION_CHOICES,
    })


@admin_required
def admin_products(request):
    """Gestion des produits du marketplace"""
    from marketplace.models import Product

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            # Get or create default seller
            seller, _ = User.objects.get_or_create(
                username='farmconnect_store',
                defaults={'email': 'store@farmconnect.sn', 'role': 'admin'}
            )

            Product.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                category=request.POST.get('category'),
                quantity_available=request.POST.get('quantity_available', 0),
                seller=seller,
                is_available=True
            )
            messages.success(request, "Produit ajouté avec succès!")

        elif action == 'update':
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')
            product.category = request.POST.get('category')
            product.quantity_available = request.POST.get('quantity_available', 0)
            product.is_available = request.POST.get('is_available') == 'on'
            product.save()
            messages.success(request, "Produit mis à jour avec succès!")

        elif action == 'delete':
            product_id = request.POST.get('product_id')
            Product.objects.filter(id=product_id).delete()
            messages.success(request, "Produit supprimé avec succès!")

        return redirect('farmconnect_app:admin_products')

    products = Product.objects.all().order_by('-created_at')
    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'admin_dashboard/products.html', {
        'products': products,
        'categories': categories,
    })


@admin_required
def admin_advice(request):
    """Gestion des conseils de cultures"""
    from advice.models import CropAdvice
    from crops.models import Crop

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            crop_id = request.POST.get('crop_id')
            crop = Crop.objects.get(id=crop_id)

            CropAdvice.objects.create(
                crop=crop,
                planting_season_fr=request.POST.get('planting_season_fr', ''),
                maturity_time_fr=request.POST.get('maturity_time_fr', ''),
                soil_type_fr=request.POST.get('soil_type_fr', ''),
                challenges_insects_fr=request.POST.get('challenges_insects_fr', ''),
                challenges_diseases_fr=request.POST.get('challenges_diseases_fr', ''),
                challenges_environmental_fr=request.POST.get('challenges_environmental_fr', ''),
                prevention_tips_fr=request.POST.get('prevention_tips_fr', ''),
                management_tips_fr=request.POST.get('management_tips_fr', ''),
                recommended_fertilizers_fr=request.POST.get('recommended_fertilizers_fr', ''),
                recommended_pesticides_fr=request.POST.get('recommended_pesticides_fr', ''),
                recommended_tools_fr=request.POST.get('recommended_tools_fr', ''),
                innovative_inputs_fr=request.POST.get('innovative_inputs_fr', ''),
                additional_notes_fr=request.POST.get('additional_notes_fr', ''),
                created_by=request.user
            )
            messages.success(request, "Conseil ajouté avec succès!")

        elif action == 'update':
            advice_id = request.POST.get('advice_id')
            advice = CropAdvice.objects.get(id=advice_id)
            advice.planting_season_fr = request.POST.get('planting_season_fr', '')
            advice.maturity_time_fr = request.POST.get('maturity_time_fr', '')
            advice.soil_type_fr = request.POST.get('soil_type_fr', '')
            advice.challenges_insects_fr = request.POST.get('challenges_insects_fr', '')
            advice.challenges_diseases_fr = request.POST.get('challenges_diseases_fr', '')
            advice.challenges_environmental_fr = request.POST.get('challenges_environmental_fr', '')
            advice.prevention_tips_fr = request.POST.get('prevention_tips_fr', '')
            advice.management_tips_fr = request.POST.get('management_tips_fr', '')
            advice.recommended_fertilizers_fr = request.POST.get('recommended_fertilizers_fr', '')
            advice.recommended_pesticides_fr = request.POST.get('recommended_pesticides_fr', '')
            advice.recommended_tools_fr = request.POST.get('recommended_tools_fr', '')
            advice.innovative_inputs_fr = request.POST.get('innovative_inputs_fr', '')
            advice.additional_notes_fr = request.POST.get('additional_notes_fr', '')
            advice.is_active = request.POST.get('is_active') == 'on'
            advice.save()
            messages.success(request, "Conseil mis à jour avec succès!")

        elif action == 'delete':
            advice_id = request.POST.get('advice_id')
            CropAdvice.objects.filter(id=advice_id).delete()
            messages.success(request, "Conseil supprimé avec succès!")

        return redirect('farmconnect_app:admin_advice')

    # Get all advice with related crops
    advice_list = CropAdvice.objects.select_related('crop').all().order_by('crop__name_fr')

    # Get crops that don't have advice yet (for adding new advice)
    crops_with_advice = CropAdvice.objects.values_list('crop_id', flat=True)
    available_crops = Crop.objects.filter(is_active=True).exclude(id__in=crops_with_advice).order_by('name_fr')

    return render(request, 'admin_dashboard/advice.html', {
        'advice_list': advice_list,
        'available_crops': available_crops,
    })


# ============================================
# TOOL ORDER VIEWS
# ============================================

@login_required
def place_order(request):
    """Vue pour passer une commande d'outil"""
    from marketplace.models import ToolOrder

    if request.method == 'POST':
        user = request.user

        # Create the order
        order = ToolOrder.objects.create(
            buyer=user,
            buyer_name=request.POST.get('buyer_name', f"{user.first_name} {user.last_name}"),
            buyer_phone=request.POST.get('buyer_phone', user.phone_number or ''),
            buyer_email=request.POST.get('buyer_email', user.email),
            buyer_region=request.POST.get('buyer_region', user.region),
            buyer_village=request.POST.get('buyer_village', user.village),
            tool_name=request.POST.get('tool_name'),
            tool_price=request.POST.get('tool_price'),
            quantity=request.POST.get('quantity', 1),
            payment_plan=request.POST.get('payment_plan', 'full'),
            message=request.POST.get('message', '')
        )

        messages.success(
            request,
            _('Votre commande #{} a été enregistrée avec succès! Un administrateur vous contactera bientôt.').format(order.id)
        )

        return redirect('farmconnect_app:my_orders')

    # GET request - show form
    tool_name = request.GET.get('tool', '')
    tool_price = request.GET.get('price', '')

    context = {
        'tool_name': tool_name,
        'tool_price': tool_price,
        'user': request.user,
    }

    return render(request, 'farmconnect_app/place_order.html', context)


@login_required
def my_orders(request):
    """Vue pour voir mes commandes"""
    from marketplace.models import ToolOrder

    orders = ToolOrder.objects.filter(buyer=request.user).order_by('-created_at')

    return render(request, 'farmconnect_app/my_orders.html', {
        'orders': orders,
    })


@admin_required
def admin_orders(request):
    """Gestion des commandes d'outils"""
    from marketplace.models import ToolOrder
    from django.utils import timezone

    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')

        try:
            order = ToolOrder.objects.get(id=order_id)

            if action == 'update_status':
                new_status = request.POST.get('status')
                order.status = new_status
                if new_status == 'contacted' and not order.contacted_at:
                    order.contacted_at = timezone.now()
                order.save()
                messages.success(request, f"Statut de la commande #{order_id} mis à jour!")

            elif action == 'add_notes':
                order.admin_notes = request.POST.get('admin_notes', '')
                order.save()
                messages.success(request, f"Notes ajoutées à la commande #{order_id}!")

            elif action == 'delete':
                order.delete()
                messages.success(request, f"Commande #{order_id} supprimée!")

        except ToolOrder.DoesNotExist:
            messages.error(request, "Commande non trouvée!")

        return redirect('farmconnect_app:admin_orders')

    # Get orders with filters
    status_filter = request.GET.get('status', '')
    orders = ToolOrder.objects.all().order_by('-created_at')

    if status_filter:
        orders = orders.filter(status=status_filter)

    # Count by status for quick filters
    status_counts = {
        'all': ToolOrder.objects.count(),
        'pending': ToolOrder.objects.filter(status='pending').count(),
        'contacted': ToolOrder.objects.filter(status='contacted').count(),
        'confirmed': ToolOrder.objects.filter(status='confirmed').count(),
        'completed': ToolOrder.objects.filter(status='completed').count(),
        'cancelled': ToolOrder.objects.filter(status='cancelled').count(),
    }

    return render(request, 'admin_dashboard/orders.html', {
        'orders': orders,
        'status_counts': status_counts,
        'current_filter': status_filter,
        'status_choices': ToolOrder.STATUS_CHOICES,
    })