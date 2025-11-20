"""
Service de stockage offline pour FarmConnect
Gère le cache des données météo, conseils agricoles et prix du marché
"""
from django.core.cache import cache
from django.conf import settings
import json
from datetime import timedelta


class OfflineStorage:
    """
    Service de stockage offline pour WeatherService, CropTips et MarketPrices
    Utilise Django cache + IndexedDB côté client
    """

    # Cache timeouts (en secondes)
    WEATHER_CACHE_TIMEOUT = 1800  # 30 minutes
    FORECAST_CACHE_TIMEOUT = 3600  # 1 heure
    TIPS_CACHE_TIMEOUT = 86400  # 24 heures
    PRICES_CACHE_TIMEOUT = 3600  # 1 heure

    @staticmethod
    def cache_weather_data(region, data):
        """
        Met en cache les données météo actuelles pour une région

        Args:
            region (str): Nom de la région
            data (dict): Données météo
        """
        cache_key = f'offline_weather_{region.lower()}'
        cache.set(cache_key, data, OfflineStorage.WEATHER_CACHE_TIMEOUT)
        return True

    @staticmethod
    def get_cached_weather(region):
        """
        Récupère les données météo en cache pour une région

        Args:
            region (str): Nom de la région

        Returns:
            dict or None: Données météo en cache ou None
        """
        cache_key = f'offline_weather_{region.lower()}'
        return cache.get(cache_key)

    @staticmethod
    def cache_forecast_data(region, data):
        """
        Met en cache les prévisions météo pour une région

        Args:
            region (str): Nom de la région
            data (dict): Données de prévisions
        """
        cache_key = f'offline_forecast_{region.lower()}'
        cache.set(cache_key, data, OfflineStorage.FORECAST_CACHE_TIMEOUT)
        return True

    @staticmethod
    def get_cached_forecast(region):
        """
        Récupère les prévisions météo en cache pour une région

        Args:
            region (str): Nom de la région

        Returns:
            dict or None: Prévisions en cache ou None
        """
        cache_key = f'offline_forecast_{region.lower()}'
        return cache.get(cache_key)

    @staticmethod
    def cache_crop_tips(tips):
        """
        Met en cache la liste des conseils agricoles

        Args:
            tips (list): Liste des conseils agricoles (serialized)
        """
        cache.set('offline_crop_tips', tips, OfflineStorage.TIPS_CACHE_TIMEOUT)
        return True

    @staticmethod
    def get_cached_tips():
        """
        Récupère les conseils agricoles en cache

        Returns:
            list: Liste des conseils agricoles ou []
        """
        return cache.get('offline_crop_tips', [])

    @staticmethod
    def cache_crop_tips_for_farmer(farmer_id, tips):
        """
        Met en cache les conseils personnalisés pour un agriculteur

        Args:
            farmer_id (int): ID de l'agriculteur
            tips (list): Liste des conseils
        """
        cache_key = f'offline_tips_farmer_{farmer_id}'
        cache.set(cache_key, tips, OfflineStorage.TIPS_CACHE_TIMEOUT)
        return True

    @staticmethod
    def get_cached_tips_for_farmer(farmer_id):
        """
        Récupère les conseils personnalisés en cache pour un agriculteur

        Args:
            farmer_id (int): ID de l'agriculteur

        Returns:
            list: Liste des conseils ou []
        """
        cache_key = f'offline_tips_farmer_{farmer_id}'
        return cache.get(cache_key, [])

    @staticmethod
    def cache_market_prices(region, prices):
        """
        Met en cache les prix du marché pour une région

        Args:
            region (str): Nom de la région
            prices (list): Liste des prix (serialized)
        """
        cache_key = f'offline_prices_{region.lower()}'
        cache.set(cache_key, prices, OfflineStorage.PRICES_CACHE_TIMEOUT)
        return True

    @staticmethod
    def get_cached_prices(region):
        """
        Récupère les prix du marché en cache pour une région

        Args:
            region (str): Nom de la région

        Returns:
            list: Liste des prix ou []
        """
        cache_key = f'offline_prices_{region.lower()}'
        return cache.get(cache_key, [])

    @staticmethod
    def cache_user_data(user_id, data):
        """
        Met en cache les données utilisateur personnalisées

        Args:
            user_id (int): ID de l'utilisateur
            data (dict): Données utilisateur
        """
        cache_key = f'offline_user_{user_id}'
        cache.set(cache_key, data, 86400)  # 24 heures
        return True

    @staticmethod
    def get_cached_user_data(user_id):
        """
        Récupère les données utilisateur en cache

        Args:
            user_id (int): ID de l'utilisateur

        Returns:
            dict or None: Données utilisateur ou None
        """
        cache_key = f'offline_user_{user_id}'
        return cache.get(cache_key)

    @staticmethod
    def clear_cache_for_region(region):
        """
        Efface tout le cache pour une région spécifique

        Args:
            region (str): Nom de la région
        """
        cache.delete(f'offline_weather_{region.lower()}')
        cache.delete(f'offline_forecast_{region.lower()}')
        cache.delete(f'offline_prices_{region.lower()}')
        return True

    @staticmethod
    def clear_all_cache():
        """
        Efface tout le cache offline
        """
        cache.clear()
        return True

    @staticmethod
    def get_cache_stats():
        """
        Retourne les statistiques du cache

        Returns:
            dict: Statistiques du cache
        """
        # Cette méthode dépend du backend de cache utilisé
        # Pour memcached ou Redis, on peut obtenir des stats
        try:
            from django.core.cache import cache as default_cache
            if hasattr(default_cache, 'get_stats'):
                return default_cache.get_stats()
            else:
                return {'message': 'Stats not available for this cache backend'}
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def prepare_offline_data_package(user):
        """
        Prépare un package de données complètes pour mode offline
        Pour un utilisateur agriculteur

        Args:
            user: Instance User

        Returns:
            dict: Package de données pour offline
        """
        package = {
            'user': {
                'id': user.id,
                'name': user.get_full_name(),
                'role': user.role,
            },
            'weather': None,
            'forecast': None,
            'tips': [],
            'prices': [],
        }

        # Si l'utilisateur est un agriculteur
        if hasattr(user, 'farmer_profile'):
            farmer = user.farmer_profile
            region = farmer.region

            # Météo
            weather = OfflineStorage.get_cached_weather(region)
            if weather:
                package['weather'] = weather

            # Prévisions
            forecast = OfflineStorage.get_cached_forecast(region)
            if forecast:
                package['forecast'] = forecast

            # Conseils
            tips = OfflineStorage.get_cached_tips_for_farmer(farmer.id)
            if tips:
                package['tips'] = tips

            # Prix
            prices = OfflineStorage.get_cached_prices(region)
            if prices:
                package['prices'] = prices

        return package
