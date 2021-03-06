from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from django.shortcuts import render
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home_page.html')

class RecipeFilter(FilterSet):
    ingredients = CharFilter(field_name='ingred_list', method='ingreds_contain')

    def ingreds_contain(self, queryset, name, value): # improve this, as slow with database of over 39k recipes
        num_user_ingreds = len(self.request.GET.get('ingredients').split())
        max_missing = self.request.GET.get('tolerance', default=0)
        try:
            max_missing = int(max_missing)
        except ValueError:
            max_missing = 0
        queryset = queryset.exclude(num_ingreds__gt=num_user_ingreds+max_missing)
        lookup = '__'.join([name, 'iregex'])
        ingreds = value.split()
        temp = Recipe.objects.none()
        for ingred in ingreds:
            ingred = ' ' + ingred.replace('_', ' ') + ' '
            temp = queryset.filter(**{lookup: ingred}).union(temp)
        queryset = temp
        return queryset.order_by('num_ingreds')

    class Meta:
        model = Recipe
        fields = ['ingredients']

class RecipeViewSet(viewsets.ModelViewSet):
    PAGINATION_THRESH = 50
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RecipeFilter
    ordering_fields = ['num_ingreds']

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer]

    def list(self, request, *args, **kwargs):
        response = super(RecipeViewSet, self).list(request, *args, **kwargs)
        ingred_param = request.GET.get('ingredients', default='')
        max_missing = request.GET.get('tolerance', default=0)
        try:
            max_missing = int(max_missing)
        except ValueError:
            max_missing = 0
        if ingred_param != '':
            indices_to_del = []
            for i, recipe in enumerate(response.data):
                recipe_ingreds = recipe['ingred_list'].split('\n')
                missing_count = 0
                for ingred in recipe_ingreds:
                    missing = True
                    for user_ingred in ingred_param.split():
                        user_ingred = user_ingred.replace('_', ' ')
                        if user_ingred in ingred:
                            missing = False
                            break
                    if missing:
                        missing_count += 1
                if missing_count > max_missing:
                    indices_to_del.append(i)
                else:
                    recipe['missing'] = missing_count
            indices_to_del.reverse()
            for i in indices_to_del:
                del response.data[i]
        if request.accepted_renderer.format == 'html':
            context = {
                'recipe_list': response.data,
                'tolerance': max_missing
            }
            if ingred_param != '':
                context['search_params'] = ingred_param.replace(' ', '+')
            if len(response.data) > self.PAGINATION_THRESH:
                page = request.GET.get('page')
                paginator = Paginator(response.data, self.PAGINATION_THRESH).get_page(page)
                context['recipe_list'] = paginator
                context['pagination'] = True
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
            if 'tol' in request.GET:
                context['tolerance'] = request.GET.get('tol')
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
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['name', 'category']
    search_fields = ['name']
