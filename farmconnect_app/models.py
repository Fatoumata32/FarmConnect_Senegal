from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Modèle utilisateur étendu pour les agriculteurs"""
    ROLE_CHOICES = [
        ('farmer', 'Agriculteur'),
        ('agent', 'Agent de Vulgarisation'),
        ('admin', 'Administrateur'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    phone_regex = RegexValidator(regex=r'\+?221\d{9}$', message="Format: '+221XXXXXXXXX'")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=False, blank=True, null=True, help_text="Numéro de téléphone au format +221XXXXXXXXX")
    region = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Taille en hectares")
    preferred_language = models.CharField(max_length=5, default='fr', choices=[('fr', 'Français'), ('wo', 'Wolof')])
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Farmer(models.Model):
    """
    Profil étendu pour les agriculteurs
    Gère les cultures, les conseils et les données météo
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Taille de l'exploitation en hectares",
        verbose_name="Taille de l'exploitation (ha)"
    )
    region = models.CharField(
        max_length=100,
        choices=[
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
        ],
        verbose_name="Région"
    )
    crops_grown = models.ManyToManyField(
        'crops.Crop',
        verbose_name="Cultures cultivées",
        related_name='farmers'
    )
    years_experience = models.IntegerField(
        default=0,
        verbose_name="Années d'expérience"
    )
    irrigation_type = models.CharField(
        max_length=50,
        choices=[
            ('none', 'Aucune'),
            ('manual', 'Manuelle'),
            ('drip', 'Goutte à goutte'),
            ('sprinkler', 'Aspersion'),
            ('flood', 'Inondation')
        ],
        default='none',
        verbose_name="Type d'irrigation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agriculteur"
        verbose_name_plural = "Agriculteurs"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_region_display()}"

    def get_crop_tips(self):
        """
        Retourne les conseils agricoles pour les cultures de l'agriculteur
        """
        from crops.models import CropTip
        tips = []
        for crop in self.crops_grown.all():
            tips.extend(list(crop.tips.all()))
        return tips

    def get_weather_data(self):
        """
        Retourne les données météo pour la région de l'agriculteur
        """
        from weather.weather_service import WeatherService
        service = WeatherService()
        return service.get_current_weather(self.region)

    def get_forecast(self):
        """
        Retourne les prévisions météo pour la région de l'agriculteur
        """
        from weather.weather_service import WeatherService
        service = WeatherService()
        return service.get_forecast(self.region, days=3)

    def get_market_prices(self):
        """
        Retourne les prix du marché pour les cultures de l'agriculteur
        """
        from community.models import MarketPrice
        crop_names = [crop.nom_francais for crop in self.crops_grown.all()]
        return MarketPrice.objects.filter(
            crop_name__in=crop_names,
            region=self.region
        ).order_by('-date')


class ExtensionAgent(models.Model):
    """
    Profil pour les agents de vulgarisation agricole
    Gère les conseils et les mises à jour
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    specialization = models.CharField(
        max_length=200,
        verbose_name="Spécialisation",
        help_text="Ex: Cultures maraîchères, Élevage, Agroforesterie"
    )
    regions_covered = models.JSONField(
        default=list,
        verbose_name="Régions couvertes",
        help_text="Liste des régions couvertes par l'agent"
    )
    organization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Organisation",
        help_text="Nom de l'organisation d'origine"
    )
    certification = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Certification",
        help_text="Diplômes et certifications"
    )
    years_experience = models.IntegerField(
        default=0,
        verbose_name="Années d'expérience"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agent de vulgarisation"
        verbose_name_plural = "Agents de vulgarisation"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"

    def create_crop_tip(self, crop, title_fr, content_fr, title_wo='', content_wo='', tip_type='care', priority=2):
        """
        Crée un nouveau conseil agricole
        """
        from crops.models import CropTip
        tip = CropTip.objects.create(
            crop=crop,
            title_fr=title_fr,
            title_wo=title_wo or title_fr,
            content_fr=content_fr,
            content_wo=content_wo or content_fr,
            tip_type=tip_type,
            priority=priority,
            created_by=self.user
        )
        return tip

    def update_crop_tip(self, tip_id, **kwargs):
        """
        Met à jour un conseil agricole existant
        """
        from crops.models import CropTip
        try:
            tip = CropTip.objects.get(id=tip_id, created_by=self.user)
            for key, value in kwargs.items():
                if hasattr(tip, key):
                    setattr(tip, key, value)
            tip.save()
            return tip
        except CropTip.DoesNotExist:
            return None

    def get_tips_stats(self):
        """
        Retourne les statistiques des conseils créés
        """
        from crops.models import CropTip
        tips = CropTip.objects.filter(created_by=self.user)
        return {
            'total': tips.count(),
            'urgent': tips.filter(is_urgent=True).count(),
            'high_priority': tips.filter(priority__gte=3).count(),
            'by_type': {
                'planting': tips.filter(tip_type='planting').count(),
                'care': tips.filter(tip_type='care').count(),
                'harvest': tips.filter(tip_type='harvest').count(),
            }
        }

    def get_farmers_in_regions(self):
        """
        Retourne les agriculteurs dans les régions couvertes
        """
        return Farmer.objects.filter(region__in=self.regions_covered)
