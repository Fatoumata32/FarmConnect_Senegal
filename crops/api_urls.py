"""
Configuration des routes pour l'API REST
Utilise le router de Django REST Framework
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Router pour les ViewSets
router = DefaultRouter()
router.register(r'crops', api_views.CropViewSet, basename='crop')
router.register(r'soil-types', api_views.SoilTypeViewSet, basename='soiltype')
router.register(r'seasons', api_views.SeasonViewSet, basename='season')
router.register(r'recommendations', api_views.RecommendationViewSet, basename='recommendation')

# URLs de l'API
urlpatterns = [
    # Routes du router (CRUD complet)
    path('', include(router.urls)),

    # Endpoints personnalisés
    path('weather/', api_views.weather_api, name='weather-api'),
    path('sync/', api_views.sync_api, name='sync-api'),
    path('stats/', api_views.api_stats, name='stats-api'),
]
