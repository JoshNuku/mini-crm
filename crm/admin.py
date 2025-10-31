from django.contrib import admin
from .models import Client, ClientInteraction


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'company', 'stage', 'created_by', 'created_at']
    list_filter = ['stage', 'created_at', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Additional Details', {
            'fields': ('address', 'notes')
        }),
        ('CRM Information', {
            'fields': ('stage', 'created_by', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClientInteraction)
class ClientInteractionAdmin(admin.ModelAdmin):
    list_display = ['client', 'interaction_type', 'subject', 'created_by', 'created_at']
    list_filter = ['interaction_type', 'created_at']
    search_fields = ['client__first_name', 'client__last_name', 'subject', 'description']
    readonly_fields = ['created_at']
