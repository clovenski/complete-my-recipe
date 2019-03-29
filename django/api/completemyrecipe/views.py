from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home_page.html')

class RecipeFilter(FilterSet):
    ingredients = CharFilter(field_name='ingred_list', method='ingreds_contain')

    def ingreds_contain(self, queryset, name, value):
        lookup = '__'.join([name, 'iregex'])
        ingreds = value.split()
        temp = Recipe.objects.none()
        for ingred in ingreds:
            temp = queryset.filter(**{lookup: ingred}).union(temp)
        queryset = temp
        return queryset

    class Meta:
        model = Recipe
        fields = ['ingredients']

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RecipeFilter
    ordering_fields = ['num_ingreds']

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer]

    def list(self, request, *args, **kwargs):
        response = super(RecipeViewSet, self).list(request, *args, **kwargs)
        ingred_param = request.GET.get('ingredients', default='')
        if ingred_param != '':
            for recipe in response.data:
                recipe_ingred = set(recipe['ingred_list'].split('\n')) # change once simplified ingred list field implemented
                recipe['missing'] = ' '.join(str(i) for i in recipe_ingred.difference(ingred_param))
        if request.accepted_renderer.format == 'html':
            context = {'recipe_list': response.data}
            if ingred_param != '':
                context['search_params'] = ingred_param.replace(' ', '+')
            response = Response(context, template_name='list_recipes.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(RecipeViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            ingred_list = response.data['ingred_list'].split('\n')
            context = {
                'name': response.data['name'],
                'num_ingreds': response.data['num_ingreds'],
                'ingredients': ingred_list,
                'instructions': response.data['instructions']
            }
            if 'params' in request.GET:
                context['search_params'] = request.GET.get('params').replace(' ', '+')
            response = Response(context, template_name='view_recipe.html')
        return response

    def create(self, request, *args, **kwargs):
        response = super(RecipeViewSet, self).create(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            ingred_list = response.data['ingred_list'].split('\n')
            context = {
                'name': response.data['name'],
                'num_ingreds': response.data['num_ingreds'],
                'ingredients': ingred_list,
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
