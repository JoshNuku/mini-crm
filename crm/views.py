from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Client, ClientInteraction
from .serializers import (
    ClientSerializer, ClientListSerializer, 
    ClientInteractionSerializer, UserSerializer
)


class IsAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing clients.
    
    list: Get all clients
    create: Create a new client
    retrieve: Get a specific client
    update: Update a client
    partial_update: Partially update a client
    destroy: Delete a client
    update_stage: Update client's onboarding stage
    """
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClientListSerializer
        return ClientSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_stage(self, request, pk=None):
        """
        Update the onboarding stage of a client.
        
        Accepts: {"stage": "LEAD" | "IN_PROGRESS" | "ACTIVE"}
        """
        client = self.get_object()
        stage = request.data.get('stage')
        
        valid_stages = ['LEAD', 'IN_PROGRESS', 'ACTIVE']
        if stage not in valid_stages:
            return Response(
                {'error': f'Invalid stage. Must be one of: {", ".join(valid_stages)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_stage = client.stage
        client.stage = stage
        client.save()
        
        ClientInteraction.objects.create(
            client=client,
            interaction_type='NOTE',
            subject=f'Stage Updated: {old_stage} → {stage}',
            description=f'Stage changed from {old_stage} to {stage} by {request.user.username}',
            created_by=request.user
        )
        
        serializer = self.get_serializer(client)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_stage(self, request):
        """
        Get clients filtered by stage.
        
        Query param: stage (LEAD, IN_PROGRESS, ACTIVE)
        """
        stage = request.query_params.get('stage')
        if stage:
            clients = self.queryset.filter(stage=stage)
        else:
            clients = self.queryset.all()
        
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data)


class ClientInteractionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing client interactions.
    """
    queryset = ClientInteraction.objects.all()
    serializer_class = ClientInteractionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user."""
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """Allow filtering interactions by client."""
        queryset = ClientInteraction.objects.all()
        client_id = self.request.query_params.get('client')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistics(request):
    """
    Get CRM statistics and reporting data.
    
    Returns:
    - Total clients count
    - Clients by stage
    - Recent clients (last 30 days)
    - Clients by assigned staff
    - Recent interactions count
    """
    total_clients = Client.objects.count()
    
    stage_stats = Client.objects.values('stage').annotate(count=Count('id'))
    clients_by_stage = {item['stage']: item['count'] for item in stage_stats}
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_clients = Client.objects.filter(created_at__gte=thirty_days_ago).count()
    
    staff_stats = Client.objects.filter(
        assigned_to__isnull=False
    ).values(
        'assigned_to__username'
    ).annotate(
        count=Count('id')
    )
    clients_by_staff = {
        item['assigned_to__username']: item['count'] 
        for item in staff_stats
    }
    
    total_interactions = ClientInteraction.objects.count()
    
    recent_interactions = ClientInteraction.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    
    lead_count = clients_by_stage.get('LEAD', 0)
    in_progress_count = clients_by_stage.get('IN_PROGRESS', 0)
    active_count = clients_by_stage.get('ACTIVE', 0)
    
    conversion_rate = 0
    if total_clients > 0:
        conversion_rate = round((active_count / total_clients) * 100, 2)
    
    return Response({
        'total_clients': total_clients,
        'clients_by_stage': {
            'lead': clients_by_stage.get('LEAD', 0),
            'in_progress': clients_by_stage.get('IN_PROGRESS', 0),
            'active': clients_by_stage.get('ACTIVE', 0),
        },
        'recent_clients_30_days': recent_clients,
        'clients_by_staff': clients_by_staff,
        'total_interactions': total_interactions,
        'recent_interactions_30_days': recent_interactions,
        'conversion_rate_percentage': conversion_rate,
        'funnel': {
            'lead': lead_count,
            'in_progress': in_progress_count,
            'active': active_count,
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user information."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
