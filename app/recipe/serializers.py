"""
Serializres for the recipe API View
"""
from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for the Ingredient object. """
    
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']
        

class TagSerializer(serializers.ModelSerializer):
    """ Serializer for the Tag object. """
    
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for the recipe object. """
    tags = TagSerializer(many=True, required=False)
    
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']
    
    def _get_or_create_tags(self, tags, recipe):
        """ Handle getting or creating tags as needed. """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
        
    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """ Update recipe """
        tags = validated_data.pop('tags', None)
        if tags is not None: #Called if is []
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
            
        return super().update(instance, validated_data)
        
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        
        # instance.save()
        # return instance
        

class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer for recipe detail view. """
    
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
        

class RecipeImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to recipes. """
    
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}