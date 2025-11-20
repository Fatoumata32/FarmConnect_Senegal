from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import WeatherData
from django.utils import timezone
from .weather_service import WeatherService
import logging

logger = logging.getLogger(__name__)


def get_current_weather(request):
    """
    API endpoint pour obtenir la météo actuelle et prévisions 3 jours
    """
    region = request.GET.get('region', 'dakar')

    try:
        # Utiliser le nouveau service météo
        weather_service = WeatherService()

        # Récupérer météo actuelle
        current = weather_service.get_current_weather(region)

        # Récupérer prévisions 3 jours
        forecast = weather_service.get_forecast_3days(region)

        # Générer conseils agricoles
        advice = weather_service.get_agricultural_advice(current, forecast)

        # Construire la réponse
        response_data = {
            'region': region.title(),
            'current': current,
            'forecast': forecast,
            'advice': advice,
            'timestamp': current.get('timestamp') if current else None
        }

        logger.info(f"[Weather API] Served data for {region}")
        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"[Weather API] Error: {e}")
        return JsonResponse({
            'error': 'Unable to fetch weather data',
            'message': str(e)
        }, status=500)

def weather_dashboard(request):
   
    regions = WeatherData.objects.values('region').distinct()
    recent_weather = WeatherData.objects.filter(is_current=True).order_by('-recorded_at')[:10]
    
    context = {
        'regions': regions,
        'recent_weather': recent_weather,
    }
    return render(request, 'weather/dashboard.html', context)