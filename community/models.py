from django.db import models
from django.conf import settings

class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class MarketPrice(models.Model):
    """
    Prix du marché pour les cultures au Sénégal
    Affiche les prix actuels, tendances et variations régionales
    """
    TREND_CHOICES = [
        ('up', 'En hausse'),
        ('down', 'En baisse'),
        ('stable', 'Stable')
    ]

    REGION_CHOICES = [
        ('dakar', 'Dakar'),
        ('thies', 'Thiès'),
        ('kaolack', 'Kaolack'),
        ('saint-louis', 'Saint-Louis'),
        ('ziguinchor', 'Ziguinchor'),
        ('tambacounda', 'Tambacounda'),
        ('kolda', 'Kolda'),
        ('matam', 'Matam'),
        ('louga', 'Louga'),
        ('fatick', 'Fatick'),
        ('diourbel', 'Diourbel'),
        ('kaffrine', 'Kaffrine'),
        ('kedougou', 'Kédougou'),
        ('sedhiou', 'Sédhiou'),
    ]

    crop_name = models.CharField(max_length=100, verbose_name="Culture")
    region = models.CharField(max_length=100, choices=REGION_CHOICES, verbose_name="Région")
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix par kg (FCFA)")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    trend = models.CharField(max_length=20, choices=TREND_CHOICES, default='stable', verbose_name="Tendance")
    percentage_change = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Changement (%)")

    class Meta:
        ordering = ['-date', 'crop_name', 'region']
        verbose_name = "Prix du marché"
        verbose_name_plural = "Prix du marché"

    def __str__(self):
        return f"{self.crop_name} - {self.get_region_display()} - {self.price_per_kg} FCFA/kg"

    def get_trend_icon(self):
        """Retourne l'icône correspondant à la tendance"""
        icons = {
            'up': 'fa-arrow-trend-up',
            'down': 'fa-arrow-trend-down',
            'stable': 'fa-minus'
        }
        return icons.get(self.trend, 'fa-minus')

    def get_trend_color(self):
        """Retourne la couleur correspondant à la tendance"""
        colors = {
            'up': '#28a745',  # Green
            'down': '#dc3545',  # Red
            'stable': '#6c757d'  # Gray
        }
        return colors.get(self.trend, '#6c757d')


class Event(models.Model):
    """
    Événements, rencontres et workshops pour la communauté agricole
    """
    EVENT_TYPE_CHOICES = [
        ('workshop', 'Atelier/Workshop'),
        ('meeting', 'Rencontre'),
        ('training', 'Formation'),
        ('fair', 'Foire agricole'),
        ('webinar', 'Webinaire'),
    ]

    REGION_CHOICES = [
        ('dakar', 'Dakar'),
        ('thies', 'Thiès'),
        ('kaolack', 'Kaolack'),
        ('saint-louis', 'Saint-Louis'),
        ('ziguinchor', 'Ziguinchor'),
        ('tambacounda', 'Tambacounda'),
        ('kolda', 'Kolda'),
        ('matam', 'Matam'),
        ('louga', 'Louga'),
        ('fatick', 'Fatick'),
        ('diourbel', 'Diourbel'),
        ('kaffrine', 'Kaffrine'),
        ('kedougou', 'Kédougou'),
        ('sedhiou', 'Sédhiou'),
        ('online', 'En ligne'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, verbose_name="Type d'événement")
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin", null=True, blank=True)
    location = models.CharField(max_length=300, verbose_name="Lieu")
    region = models.CharField(max_length=100, choices=REGION_CHOICES, verbose_name="Région")
    organizer = models.CharField(max_length=200, verbose_name="Organisateur")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone de contact")
    contact_email = models.EmailField(blank=True, verbose_name="Email de contact")
    max_participants = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nombre max de participants")
    is_free = models.BooleanField(default=True, verbose_name="Gratuit")
    registration_required = models.BooleanField(default=False, verbose_name="Inscription requise")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"

    def __str__(self):
        return f"{self.title} - {self.date}"

    def get_event_type_icon(self):
        """Retourne l'icône correspondant au type d'événement"""
        icons = {
            'workshop': 'fa-tools',
            'meeting': 'fa-users',
            'training': 'fa-graduation-cap',
            'fair': 'fa-store',
            'webinar': 'fa-video',
        }
        return icons.get(self.event_type, 'fa-calendar')

    def get_event_type_color(self):
        """Retourne la couleur correspondant au type d'événement"""
        colors = {
            'workshop': '#2d5016',
            'meeting': '#4a7c59',
            'training': '#f4d03f',
            'fair': '#e67e22',
            'webinar': '#3498db',
        }
        return colors.get(self.event_type, '#2d5016')