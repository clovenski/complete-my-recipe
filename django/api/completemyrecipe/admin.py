from django.contrib import admin
from .models import Recipe, Ingredient

# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['num_ingreds']
    list_display = ['name', 'id', 'num_ingreds']
    search_fields = ['ingred_list']

class IngredientAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['id', 'name', 'category']
    search_fields = ['name']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
