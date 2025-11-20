from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Farmer, ExtensionAgent


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations FarmConnect', {
            'fields': ('role', 'phone_number', 'region', 'village', 'farm_size',
                      'preferred_language', 'profile_picture', 'is_verified', 'birth_date')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'region', 'is_verified', 'date_joined')
    list_filter = ('role', 'region', 'is_verified', 'preferred_language', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'region', 'village')
    ordering = ('-date_joined',)


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'farm_size', 'years_experience', 'irrigation_type', 'created_at')
    list_filter = ('region', 'irrigation_type', 'years_experience')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'region')
    filter_horizontal = ('crops_grown',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Exploitation', {
            'fields': ('farm_size', 'region', 'crops_grown', 'irrigation_type')
        }),
        ('Expérience', {
            'fields': ('years_experience',)
        }),
    )


@admin.register(ExtensionAgent)
class ExtensionAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'organization', 'years_experience', 'created_at')
    list_filter = ('years_experience', 'organization')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization', 'organization')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Profil Professionnel', {
            'fields': ('specialization', 'organization', 'certification', 'years_experience')
        }),
        ('Zones d\'Intervention', {
            'fields': ('regions_covered',)
        }),
    )
