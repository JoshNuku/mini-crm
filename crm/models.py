from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    
    STAGE_CHOICES = [
        ('LEAD', 'Lead'),
        ('IN_PROGRESS', 'In Progress'),
        ('ACTIVE', 'Active'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(blank=True, max_length=12)
    company = models.CharField(max_length=200, blank=True)
    
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='LEAD'
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_clients'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_clients'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.stage}"


class ClientInteraction(models.Model):
    
    INTERACTION_TYPES = [
        ('CALL', 'Phone Call'),
        ('EMAIL', 'Email'),
        ('MEETING', 'Meeting'),
        ('NOTE', 'Note'),
    ]
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES
    )
    subject = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.client} - {self.interaction_type} - {self.created_at}"
