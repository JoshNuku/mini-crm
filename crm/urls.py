from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, ClientInteractionViewSet,
    statistics, current_user
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'interactions', ClientInteractionViewSet, basename='interaction')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', statistics, name='statistics'),
    path('me/', current_user, name='current-user'),
]
