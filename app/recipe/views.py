"""
Views for the Recipe API
"""
from rest_framework import (
    viewsets,
    authentication,
    permissions,
    mixins
)

from recipe import serializers
from core.models import Recipe, Tag, Ingredient


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
        
        
class BaseRecipeAttrViewSet(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """ Base class for recipe ViewSets """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    

class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredients in the database. """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    