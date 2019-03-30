from .models import Recipe, Ingredient
from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = HashidSerializerCharField(source_field='completemyrecipe.Recipe.id', read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingred_list', 'instructions', 'num_ingreds',)

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    id = HashidSerializerCharField(source_field='completemyrecipe.Ingredient.id', read_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'category',)
