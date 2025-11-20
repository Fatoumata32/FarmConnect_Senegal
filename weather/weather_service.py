"""
Service pour récupérer les données météo depuis WeatherAPI.com
"""
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import logging
import locale

# Set French locale for date formatting
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'French_France.1252')  # Windows
    except locale.Error:
        pass  # Fall back to default locale

logger = logging.getLogger(__name__)


class WeatherService:
    """Service de récupération des données météo via OpenWeather API"""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    # Coordonnées des principales régions du Sénégal
    REGIONS = {
        'dakar': {'lat': 14.7167, 'lon': -17.4677},
        'thies': {'lat': 14.7886, 'lon': -16.9262},
        'saint-louis': {'lat': 16.0178, 'lon': -16.4897},
        'diourbel': {'lat': 14.6542, 'lon': -16.2345},
        'louga': {'lat': 15.6142, 'lon': -16.2302},
        'fatick': {'lat': 14.3386, 'lon': -16.4077},
        'kaolack': {'lat': 14.1510, 'lon': -16.0711},
        'kaffrine': {'lat': 14.1064, 'lon': -15.5518},
        'tambacounda': {'lat': 13.7707, 'lon': -13.6709},
        'kedougou': {'lat': 12.5574, 'lon': -12.1754},
        'kolda': {'lat': 12.8940, 'lon': -14.9505},
        'sedhiou': {'lat': 12.7076, 'lon': -15.5569},
        'ziguinchor': {'lat': 12.5681, 'lon': -16.2739},
        'matam': {'lat': 15.6538, 'lon': -13.2558},
    }

    def __init__(self):
        # Use OpenWeather API key
        self.api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')

    def get_current_weather(self, region='dakar'):
        """
        Récupère la météo actuelle pour une région

        Args:
            region: Nom de la région (défaut: dakar)

        Returns:
            dict: Données météo ou None si erreur
        """
        # Vérifier le cache (30 minutes)
        cache_key = f'weather_current_{region}'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"[Weather] Cache hit for {region}")
            return cached_data

        # Si pas de clé API, retourner des données simulées
        if not self.api_key or self.api_key == '':
            logger.warning("[Weather] No API key configured, using simulated data")
            return self._get_simulated_weather(region)

        # Récupérer depuis l'API OpenWeather
        coords = self.REGIONS.get(region.lower(), self.REGIONS['dakar'])

        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric',  # For Celsius
                'lang': 'fr'
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            # Formater les données depuis OpenWeather
            weather_data = {
                'region': region.title(),
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'temp_min': round(data['main']['temp_min'], 1),
                'temp_max': round(data['main']['temp_max'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s to km/h
                'wind_direction': data['wind'].get('deg', 0),
                'cloudiness': data['clouds']['all'],
                'visibility': round(data.get('visibility', 10000) / 1000, 1),  # meters to km
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'rain_1h': data.get('rain', {}).get('1h', 0),
                'timestamp': datetime.now().isoformat(),
            }

            # Mettre en cache pour 30 minutes
            cache.set(cache_key, weather_data, 1800)
            logger.info(f"[Weather] Fetched fresh data for {region} from OpenWeather")

            return weather_data

        except requests.exceptions.RequestException as e:
            logger.error(f"[Weather] OpenWeather API error for {region}: {e}")
            return self._get_simulated_weather(region)
        except Exception as e:
            logger.error(f"[Weather] Unexpected error: {e}")
            return self._get_simulated_weather(region)

    def get_forecast_3days(self, region='dakar'):
        """
        Récupère les prévisions sur 3 jours

        Args:
            region: Nom de la région

        Returns:
            list: Liste de 3 prévisions journalières
        """
        # Vérifier le cache (1 heure)
        cache_key = f'weather_forecast_{region}'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"[Weather] Forecast cache hit for {region}")
            return cached_data

        # Si pas de clé API, retourner des données simulées
        if not self.api_key or self.api_key == '':
            return self._get_simulated_forecast(region)

        coords = self.REGIONS.get(region.lower(), self.REGIONS['dakar'])

        try:
            url = f"{self.BASE_URL}/forecast"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'fr',
                'cnt': 24  # 3 days * 8 (3-hour intervals)
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            # Convertir les données OpenWeather en format compatible
            daily_forecasts = self._format_openweather_forecast(data['list'])

            # Mettre en cache pour 1 heure
            cache.set(cache_key, daily_forecasts, 3600)
            logger.info(f"[Weather] Fetched forecast for {region} from OpenWeather")

            return daily_forecasts[:3]  # Retourner seulement 3 jours

        except Exception as e:
            logger.error(f"[Weather] Forecast error: {e}")
            return self._get_simulated_forecast(region)

    def _format_openweather_forecast(self, forecast_list):
        """Formate les prévisions OpenWeather pour compatibilité (groupées par jour)"""
        from collections import defaultdict

        # Group forecasts by day
        daily_data = defaultdict(list)

        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()
            daily_data[date].append(item)

        # Format daily forecasts
        result = []
        for date, items in sorted(daily_data.items())[:3]:
            temps = [item['main']['temp'] for item in items]
            humidities = [item['main']['humidity'] for item in items]
            rain_amounts = [item.get('rain', {}).get('3h', 0) for item in items]
            wind_speeds = [item['wind']['speed'] * 3.6 for item in items]  # m/s to km/h

            # Get most common weather description
            descriptions = [item['weather'][0]['description'] for item in items]
            description = max(set(descriptions), key=descriptions.count)

            # Get icon from midday forecast if available
            icon = items[len(items)//2]['weather'][0]['icon']

            result.append({
                'date': date.isoformat(),
                'date_formatted': date.strftime('%A %d %B'),
                'temp_min': round(min(temps), 1),
                'temp_max': round(max(temps), 1),
                'temp_avg': round(sum(temps) / len(temps), 1),
                'humidity': round(sum(humidities) / len(humidities)),
                'rain_total': round(sum(rain_amounts), 1),
                'rain_chance': 100 if sum(rain_amounts) > 0 else 0,
                'description': description,
                'icon': icon,
                'wind_speed': round(max(wind_speeds), 1),
            })

        return result

    def _get_simulated_weather(self, region):
        """Retourne des données météo simulées pour le développement"""
        import random

        base_temp = 28 + random.randint(-3, 3)

        return {
            'region': region.title(),
            'temperature': base_temp,
            'feels_like': base_temp + 2,
            'temp_min': base_temp - 4,
            'temp_max': base_temp + 4,
            'humidity': 65 + random.randint(-10, 10),
            'pressure': 1013,
            'wind_speed': 15 + random.randint(-5, 5),
            'wind_direction': random.randint(0, 360),
            'cloudiness': random.randint(20, 60),
            'visibility': 10,
            'description': random.choice(['Ensoleillé', 'Partiellement nuageux', 'Nuageux']),
            'icon': '01d',
            'rain_1h': 0,
            'timestamp': datetime.now().isoformat(),
        }

    def _get_simulated_forecast(self, region):
        """Retourne des prévisions simulées sur 3 jours"""
        import random

        forecasts = []
        base_date = datetime.now().date()

        for i in range(3):
            date = base_date + timedelta(days=i)
            base_temp = 28 + random.randint(-3, 3)

            forecasts.append({
                'date': date.isoformat(),
                'date_formatted': date.strftime('%A %d %B'),
                'temp_min': base_temp - 6,
                'temp_max': base_temp + 4,
                'temp_avg': base_temp,
                'humidity': 65 + random.randint(-15, 15),
                'rain_total': random.choice([0, 0, 0, 5, 10, 15]),
                'rain_chance': random.randint(10, 70),
                'description': random.choice(['Ensoleillé', 'Partiellement nuageux', 'Pluie légère']),
                'icon': random.choice(['01d', '02d', '03d', '10d']),
                'wind_speed': 15 + random.randint(-5, 10),
            })

        return forecasts

    def get_agricultural_advice(self, weather_data, forecast_data):
        """
        Génère des conseils agricoles basés sur la météo

        Args:
            weather_data: Données météo actuelles
            forecast_data: Prévisions sur 3 jours

        Returns:
            dict: Conseils personnalisés
        """
        advice = {
            'today': [],
            'week': [],
            'alerts': []
        }

        # Conseils pour aujourd'hui
        if weather_data:
            temp = weather_data['temperature']
            humidity = weather_data['humidity']

            if temp > 35:
                advice['today'].append({
                    'icon': 'fa-sun',
                    'type': 'warning',
                    'text': f"Températures élevées ({temp}°C). Arrosez vos cultures tôt le matin ou tard le soir."
                })

            if humidity < 40:
                advice['today'].append({
                    'icon': 'fa-tint',
                    'type': 'info',
                    'text': f"Faible humidité ({humidity}%). Surveillez l'hydratation de vos plants."
                })

            if weather_data['wind_speed'] > 30:
                advice['today'].append({
                    'icon': 'fa-wind',
                    'type': 'warning',
                    'text': "Vents forts. Protégez les jeunes plants et reportez les traitements."
                })

        # Conseils pour la semaine
        if forecast_data and len(forecast_data) > 0:
            total_rain = sum(day['rain_total'] for day in forecast_data)
            avg_temp = sum(day['temp_avg'] for day in forecast_data) / len(forecast_data)

            if total_rain > 20:
                advice['week'].append({
                    'icon': 'fa-cloud-rain',
                    'type': 'success',
                    'text': f"Pluies prévues ({total_rain}mm). Bon moment pour les semis."
                })
                advice['alerts'].append({
                    'type': 'success',
                    'title': 'Conditions favorables',
                    'text': 'Les précipitations prévues fourniront une irrigation naturelle.'
                })
            elif total_rain < 5:
                advice['week'].append({
                    'icon': 'fa-tint-slash',
                    'type': 'warning',
                    'text': "Peu de pluies prévues. Planifiez l'irrigation."
                })

            if avg_temp > 30:
                advice['week'].append({
                    'icon': 'fa-thermometer-full',
                    'type': 'info',
                    'text': f"Températures élevées (moy. {round(avg_temp)}°C). Privilégiez les cultures résistantes à la chaleur."
                })

        # Conseil général si aucun conseil spécifique
        if len(advice['today']) == 0:
            advice['today'].append({
                'icon': 'fa-check-circle',
                'type': 'success',
                'text': "Conditions favorables pour les travaux aux champs."
            })

        return advice
