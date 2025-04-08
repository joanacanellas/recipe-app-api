"""
Views for the Recipe API
"""
from rest_framework import viewsets, authentication, permissions

from recipe import serializers
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """ View for manage recipe APIS. """
    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """ Retrieve recipes for authenticated users. """
        return self.request.user.recipes.all().order_by('-id')
    
    def get_serializer_class(self):
        """ Return the serializer class for request. """
        if self.action == 'list':
            return serializers.RecipeSerializer
        else:
            return self.serializer_class
    
    def perform_create(self, serializer):
        """ Create a new recipe assigned to the auth user."""
        serializer.save(user=self.request.user)