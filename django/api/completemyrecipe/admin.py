from django.contrib import admin
from .models import Recipe, Ingredient

# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['num_ingreds']
    list_display = ['name', 'id', 'num_ingreds']
    search_fields = ['ingred_list']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
