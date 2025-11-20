"""
ViewSets pour l'API REST de FarmConnect
Gère toutes les opérations CRUD via l'API
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Crop, SoilType, Season, CropSoilRecommendation, CropTip
from .serializers import (
    CropListSerializer,
    CropDetailSerializer,
    SoilTypeSerializer,
    SeasonSerializer,
    CropSoilRecommendationSerializer,
    CropSoilRecommendationListSerializer,
    CropTipSerializer
)


class CropViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet pour les cultures

    Liste et détails des cultures disponibles

    Filtres disponibles:
    - category: Filtrer par catégorie (cereales, legumes, fruits, etc.)
    - season: Filtrer par saison de culture
    - drought_resistant: true/false
    - search: Rechercher dans nom_fr, nom_wo, scientific_name
    """
    queryset = Crop.objects.filter(is_active=True).prefetch_related('suitable_soil_types', 'tips')
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name_fr', 'name_wo', 'scientific_name', 'description_fr']
    ordering_fields = ['name_fr', 'created_at', 'growth_duration_days']
    ordering = ['name_fr']

    def get_serializer_class(self):
        """Utiliser un serializer différent pour la liste et le détail"""
        if self.action == 'retrieve':
            return CropDetailSerializer
        return CropListSerializer

    def get_queryset(self):
        """Filtrer le queryset selon les paramètres"""
        queryset = super().get_queryset()

        # Filtrer par catégorie
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Filtrer par saison
        season = self.request.query_params.get('season', None)
        if season:
            queryset = queryset.filter(growing_season__icontains=season)

        # Filtrer par résistance à la sécheresse
        drought_resistant = self.request.query_params.get('drought_resistant', None)
        if drought_resistant is not None:
            queryset = queryset.filter(drought_resistant=drought_resistant.lower() == 'true')

        # Filtrer par besoin en eau
        water_requirement = self.request.query_params.get('water_requirement', None)
        if water_requirement:
            queryset = queryset.filter(water_requirement=water_requirement)

        return queryset

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        """
        Récupérer les recommandations pour une culture spécifique

        Paramètres optionnels:
        - soil_type: ID du type de sol
        - season: ID de la saison
        """
        crop = self.get_object()
        recommendations = CropSoilRecommendation.objects.filter(
            crop=crop,
            is_active=True
        ).select_related('soil_type', 'season')

        # Filtrer par type de sol si spécifié
        soil_type_id = request.query_params.get('soil_type', None)
        if soil_type_id:
            recommendations = recommendations.filter(soil_type_id=soil_type_id)

        # Filtrer par saison si spécifiée
        season_id = request.query_params.get('season', None)
        if season_id:
            recommendations = recommendations.filter(season_id=season_id)

        serializer = CropSoilRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def tips(self, request, pk=None):
        """Récupérer les conseils pour une culture spécifique"""
        crop = self.get_object()
        tips = CropTip.objects.filter(crop=crop).order_by('-priority', '-created_at')

        # Filtrer par type de conseil si spécifié
        tip_type = request.query_params.get('type', None)
        if tip_type:
            tips = tips.filter(tip_type=tip_type)

        # Filtrer par urgence
        urgent_only = request.query_params.get('urgent', None)
        if urgent_only and urgent_only.lower() == 'true':
            tips = tips.filter(is_urgent=True)

        serializer = CropTipSerializer(tips, many=True)
        return Response(serializer.data)


class SoilTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet pour les types de sol

    Liste et détails des types de sol du Sénégal

    Filtres disponibles:
    - texture: argileuse, sableuse, limoneuse, mixte
    - drainage: excellent, bon, moyen, faible
    - fertility: très_élevée, élevée, moyenne, faible
    """
    queryset = SoilType.objects.all().order_by('name_fr')
    serializer_class = SoilTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name_fr', 'name_wo', 'description_fr']

    def get_queryset(self):
        """Filtrer le queryset selon les paramètres"""
        queryset = super().get_queryset()

        # Filtrer par texture
        texture = self.request.query_params.get('texture', None)
        if texture:
            queryset = queryset.filter(texture=texture)

        # Filtrer par drainage
        drainage = self.request.query_params.get('drainage', None)
        if drainage:
            queryset = queryset.filter(drainage=drainage)

        # Filtrer par fertilité
        fertility = self.request.query_params.get('fertility', None)
        if fertility:
            queryset = queryset.filter(fertility=fertility)

        return queryset

    @action(detail=True, methods=['get'])
    def crops(self, request, pk=None):
        """Récupérer les cultures adaptées à ce type de sol"""
        soil_type = self.get_object()
        crops = soil_type.crops.filter(is_active=True)

        serializer = CropListSerializer(crops, many=True)
        return Response(serializer.data)


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet pour les saisons agricoles

    Liste et détails des saisons au Sénégal
    """
    queryset = Season.objects.all().order_by('start_month')
    serializer_class = SeasonSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def crops(self, request, pk=None):
        """Récupérer les cultures appropriées pour cette saison"""
        season = self.get_object()
        season_name = season.name_fr

        # Rechercher les cultures dont la saison correspond
        crops = Crop.objects.filter(
            Q(growing_season__icontains=season_name) | Q(growing_season__icontains='Toute l\'année'),
            is_active=True
        )

        serializer = CropListSerializer(crops, many=True)
        return Response(serializer.data)


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet pour les recommandations culture-sol

    Filtres disponibles:
    - crop: ID de la culture
    - soil_type: ID du type de sol
    - season: ID de la saison
    """
    queryset = CropSoilRecommendation.objects.filter(is_active=True).select_related(
        'crop', 'soil_type', 'season'
    ).order_by('-priority', 'crop__name_fr')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """Utiliser un serializer différent pour la liste et le détail"""
        if self.action == 'retrieve':
            return CropSoilRecommendationSerializer
        return CropSoilRecommendationListSerializer

    def get_queryset(self):
        """Filtrer le queryset selon les paramètres"""
        queryset = super().get_queryset()

        # Filtrer par culture
        crop_id = self.request.query_params.get('crop', None)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)

        # Filtrer par type de sol
        soil_type_id = self.request.query_params.get('soil_type', None)
        if soil_type_id:
            queryset = queryset.filter(soil_type_id=soil_type_id)

        # Filtrer par saison
        season_id = self.request.query_params.get('season', None)
        if season_id:
            queryset = queryset.filter(season_id=season_id)

        return queryset


@api_view(['GET'])
def weather_api(request):
    """
    API pour récupérer les données météo

    Paramètres:
    - region: Nom de la région (ex: Dakar, Thiès, Saint-Louis)

    Retourne les données météo actuelles et prévisions sur 3 jours
    """
    region = request.GET.get('region', 'Dakar').lower()

    try:
        # Utiliser le service météo avec OpenWeather API
        from weather.weather_service import WeatherService
        import logging

        logger = logging.getLogger(__name__)
        weather_service = WeatherService()

        # Récupérer météo actuelle
        current = weather_service.get_current_weather(region)

        # Récupérer prévisions 3 jours
        forecast = weather_service.get_forecast_3days(region)

        # Construire la réponse compatible avec le frontend
        data = {
            'region': region,
            'temperature': current.get('temperature'),
            'humidity': current.get('humidity'),
            'wind_speed': current.get('wind_speed'),
            'rain_chance': forecast[0].get('rain_chance', 0) if forecast else 0,
            'visibility': current.get('visibility'),
            'condition': current.get('description', 'Ensoleillé'),
            'timestamp': current.get('timestamp'),
            'forecast': forecast
        }

        logger.info(f"[Weather API] Served OpenWeather data for {region}")
        return Response(data)

    except Exception as e:
        # Fallback to simulated data if OpenWeather fails
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"[Weather API] OpenWeather failed for {region}, using simulated data: {e}")

        # Use simulated data as fallback
        data = get_simulated_weather(region)
        data['forecast'] = generate_forecast(region, 3)
        return Response(data)


def get_simulated_weather(region):
    """Génère des données météo simulées"""
    import random

    base_temps = {
        'Dakar': 28,
        'Thiès': 27,
        'Saint-Louis': 30,
        'Diourbel': 32,
        'Louga': 31,
        'Fatick': 29,
        'Kaolack': 33,
        'Kaffrine': 34,
        'Tambacounda': 35,
        'Kédougou': 34,
        'Kolda': 32,
        'Sédhiou': 31,
        'Ziguinchor': 30,
        'Matam': 33
    }

    temp = base_temps.get(region, 28)

    return {
        'region': region,
        'temperature': temp + random.uniform(-2, 2),
        'humidity': random.randint(40, 80),
        'wind_speed': random.randint(5, 25),
        'rain_chance': random.randint(0, 60),
        'visibility': random.randint(8, 10),
        'condition': random.choice([
            'Ensoleillé',
            'Partiellement nuageux',
            'Nuageux',
            'Brumeux'
        ]),
        'timestamp': timezone.now().isoformat()
    }


def generate_forecast(region, days=3):
    """Génère des prévisions météo sur plusieurs jours"""
    import random

    forecasts = []
    current_date = datetime.now().date()

    for i in range(1, days + 1):
        date = current_date + timedelta(days=i)
        forecasts.append({
            'date': date.isoformat(),
            'temp_min': random.randint(20, 25),
            'temp_max': random.randint(28, 35),
            'condition': random.choice([
                'Ensoleillé',
                'Partiellement nuageux',
                'Nuageux',
                'Risque de pluie'
            ]),
            'rain_chance': random.randint(0, 70),
            'humidity': random.randint(40, 80)
        })

    return forecasts


@api_view(['POST'])
def sync_api(request):
    """
    API pour synchroniser les données créées hors-ligne

    Corps de la requête (JSON):
    {
        "type": "favorite|note|...",
        "data": { ... }
    }
    """
    data_type = request.data.get('type')
    data = request.data.get('data')

    if not data_type or not data:
        return Response(
            {'success': False, 'message': 'Type et données requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Traiter selon le type de données
        if data_type == 'favorite':
            # TODO: Implémenter la logique des favoris
            # from farmconnect_app.models import FavoriteCrop
            # FavoriteCrop.objects.create(...)
            pass

        elif data_type == 'note':
            # TODO: Implémenter la logique des notes
            pass

        elif data_type == 'tip_feedback':
            # TODO: Implémenter la logique des feedbacks
            pass

        else:
            return Response(
                {'success': False, 'message': f'Type "{data_type}" non supporté'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'success': True,
            'message': 'Données synchronisées avec succès',
            'timestamp': timezone.now().isoformat()
        })

    except Exception as e:
        return Response(
            {'success': False, 'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def api_stats(request):
    """
    API pour récupérer les statistiques globales

    Retourne:
    - Nombre de cultures
    - Nombre de types de sol
    - Nombre de saisons
    - Nombre de recommandations
    """
    stats = {
        'crops_count': Crop.objects.filter(is_active=True).count(),
        'soil_types_count': SoilType.objects.count(),
        'seasons_count': Season.objects.count(),
        'recommendations_count': CropSoilRecommendation.objects.filter(is_active=True).count(),
        'tips_count': CropTip.objects.count(),

        # Par catégorie
        'crops_by_category': {},
        'crops_by_season': {},
    }

    # Compter par catégorie
    from django.db.models import Count
    categories = Crop.objects.filter(is_active=True).values('category').annotate(count=Count('id'))
    for cat in categories:
        stats['crops_by_category'][cat['category']] = cat['count']

    # Compter par saison
    seasons = Crop.objects.filter(is_active=True).values('growing_season').annotate(count=Count('id'))
    for season in seasons:
        stats['crops_by_season'][season['growing_season']] = season['count']

    return Response(stats)
