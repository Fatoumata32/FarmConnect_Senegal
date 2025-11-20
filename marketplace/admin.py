from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'quantity_available', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'description', 'seller__username', 'category')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('price', 'quantity_available', 'is_available')

    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Vendeur et prix', {
            'fields': ('seller', 'price', 'quantity_available')
        }),
        ('Disponibilité', {
            'fields': ('is_available',)
        }),
    )

    readonly_fields = ('created_at',)

    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, f"{queryset.count()} produit(s) marqué(s) comme disponible(s).")
    make_available.short_description = "Marquer comme disponible"

    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, f"{queryset.count()} produit(s) marqué(s) comme indisponible(s).")
    make_unavailable.short_description = "Marquer comme indisponible"
