from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

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

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer]

    def list(self, request, *args, **kwargs):
        response = super(RecipeViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            context = {'recipe_list': response.data}
            response = Response(context, template_name='list_recipes.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(RecipeViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            context = {
                'name': response.data['name'],
                'num_ingreds': response.data['num_ingreds'],
                'ingredients': response.data['ingred_list'],
                'instructions': response.data['instructions']
                }
            response = Response(context, template_name='view_recipe.html')
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['name', 'category']
    search_fields = ['name']
