from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

# Create your views here.

class RecipeFilter(FilterSet):
    ingredients = CharFilter(field_name='ingred_list', method='ingreds_contain')

    def ingreds_contain(self, queryset, name, value):
        lookup = '__'.join([name, 'iregex'])
        ingreds = value.split()
        temp = queryset.filter(**{lookup: ingreds[0]})
        for ingred in ingreds[1:]:
            temp = queryset.filter(**{lookup: ingred}).union(temp)
        queryset = temp
        return queryset

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients']

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RecipeFilter
    ordering_fields = ['num_ingreds']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['name', 'category']
    search_fields = ['name']
