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
