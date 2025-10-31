from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, ClientInteraction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ClientInteractionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ClientInteraction
        fields = [
            'id', 'client', 'interaction_type', 'subject', 
            'description', 'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']


class ClientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    interactions = ClientInteractionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'company',
            'address', 'notes', 'stage', 'created_by', 'created_by_name',
            'assigned_to', 'assigned_to_name', 'created_at', 'updated_at',
            'interactions'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class ClientListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing clients without interactions."""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'company',
            'stage', 'created_by_name', 'assigned_to_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
