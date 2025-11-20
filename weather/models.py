from django.db import models

class WeatherData(models.Model):
    """Données météorologiques pour les régions du Sénégal"""
    region = models.CharField(max_length=100, verbose_name="Région")
    temperature = models.FloatField(verbose_name="Température (°C)")
    feels_like = models.FloatField(null=True, blank=True, verbose_name="Ressenti (°C)")
    temp_min = models.FloatField(null=True, blank=True, verbose_name="Temp. min (°C)")
    temp_max = models.FloatField(null=True, blank=True, verbose_name="Temp. max (°C)")
    humidity = models.FloatField(verbose_name="Humidité (%)")
    pressure = models.FloatField(null=True, blank=True, verbose_name="Pression (hPa)")
    wind_speed = models.FloatField(null=True, blank=True, verbose_name="Vitesse du vent (km/h)")
    wind_direction = models.IntegerField(null=True, blank=True, verbose_name="Direction du vent (degrés)")
    cloudiness = models.IntegerField(null=True, blank=True, verbose_name="Nébulosité (%)")
    visibility = models.FloatField(null=True, blank=True, verbose_name="Visibilité (km)")
    description = models.CharField(max_length=200, blank=True, verbose_name="Description")
    icon = models.CharField(max_length=10, blank=True, verbose_name="Icône météo")
    rain_1h = models.FloatField(default=0, verbose_name="Pluie dernière heure (mm)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Horodatage")
    recorded_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Enregistré le")
    is_current = models.BooleanField(default=True, verbose_name="Données actuelles")

    class Meta:
        verbose_name = "Donnée météorologique"
        verbose_name_plural = "Données météorologiques"
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['region', '-recorded_at']),
            models.Index(fields=['is_current', '-recorded_at']),
        ]

    def __str__(self):
        return f"Météo à {self.region} - {self.recorded_at.strftime('%d/%m/%Y %H:%M')}"