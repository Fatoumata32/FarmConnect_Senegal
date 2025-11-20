from django.contrib import admin
from .models import ForumPost, MarketPrice, Event


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'region', 'price_per_kg', 'trend', 'percentage_change', 'date')
    list_filter = ('region', 'trend', 'date', 'crop_name')
    search_fields = ('crop_name', 'region')
    date_hierarchy = 'date'
    ordering = ('-date', 'crop_name')
    list_editable = ('price_per_kg', 'trend', 'percentage_change')

    fieldsets = (
        ('Information Générale', {
            'fields': ('crop_name', 'region')
        }),
        ('Prix et Tendance', {
            'fields': ('price_per_kg', 'trend', 'percentage_change')
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'start_time', 'region', 'organizer', 'is_active')
    list_filter = ('event_type', 'region', 'is_active', 'is_free', 'date')
    search_fields = ('title', 'description', 'organizer', 'location')
    date_hierarchy = 'date'
    ordering = ('date', 'start_time')
    list_editable = ('is_active',)

    fieldsets = (
        ('Information Générale', {
            'fields': ('title', 'description', 'event_type')
        }),
        ('Date et Heure', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Lieu', {
            'fields': ('location', 'region')
        }),
        ('Organisation', {
            'fields': ('organizer', 'contact_phone', 'contact_email')
        }),
        ('Paramètres', {
            'fields': ('max_participants', 'is_free', 'registration_required', 'is_active', 'created_by')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
