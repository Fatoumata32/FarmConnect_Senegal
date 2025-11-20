from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdviceEntryViewSet,
    DecisionTreeViewSet,
    SavedAdviceViewSet,
    CropAdviceViewSet,
    advice_library,
    crop_advice_guide,
    weather_based_advice
)

app_name = 'advice'

# Create router for API endpoints
router = DefaultRouter()
router.register(r'advice', AdviceEntryViewSet, basename='advice')
router.register(r'decision-trees', DecisionTreeViewSet, basename='decision-tree')
router.register(r'saved', SavedAdviceViewSet, basename='saved-advice')
router.register(r'crop-advice', CropAdviceViewSet, basename='crop-advice')

urlpatterns = [
    # Template views
    path('conseils/', advice_library, name='library'),
    path('guide-cultures/', crop_advice_guide, name='crop-guide'),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/weather-advice/', weather_based_advice, name='weather-advice'),
]
