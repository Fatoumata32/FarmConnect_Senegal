from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    quantity_available = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ToolOrder(models.Model):
    """Commande d'outils agricoles"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('contacted', 'Contacté'),
        ('confirmed', 'Confirmé'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]

    PAYMENT_PLAN_CHOICES = [
        ('full', 'Paiement unique'),
        ('2_installments', '2 tranches'),
        ('3_installments', '3 tranches'),
        ('4_installments', '4 tranches'),
    ]

    # Buyer information
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tool_orders',
        verbose_name="Acheteur"
    )
    buyer_name = models.CharField(max_length=200, verbose_name="Nom complet")
    buyer_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    buyer_email = models.EmailField(blank=True, verbose_name="Email")
    buyer_region = models.CharField(max_length=100, verbose_name="Région")
    buyer_village = models.CharField(max_length=200, blank=True, verbose_name="Village/Quartier")

    # Product information
    tool_name = models.CharField(max_length=300, verbose_name="Nom de l'outil")
    tool_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    payment_plan = models.CharField(
        max_length=20,
        choices=PAYMENT_PLAN_CHOICES,
        default='full',
        verbose_name="Plan de paiement"
    )

    # Order details
    message = models.TextField(blank=True, verbose_name="Message/Notes")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )
    admin_notes = models.TextField(blank=True, verbose_name="Notes de l'admin")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    contacted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de contact")

    class Meta:
        verbose_name = "Commande d'outil"
        verbose_name_plural = "Commandes d'outils"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande #{self.id} - {self.tool_name} par {self.buyer_name}"

    def get_total_price(self):
        return self.tool_price * self.quantity

    def get_status_color(self):
        colors = {
            'pending': '#ffc107',
            'contacted': '#17a2b8',
            'confirmed': '#28a745',
            'completed': '#6c757d',
            'cancelled': '#dc3545',
        }
        return colors.get(self.status, '#6c757d')