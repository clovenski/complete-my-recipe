from django.db import models
from hashid_field import HashidAutoField

HASH_ID_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'

class Recipe(models.Model):
    id = HashidAutoField(primary_key=True, alphabet=HASH_ID_ALPHABET)
    name = models.CharField(max_length=100)
    ingred_list = models.TextField(max_length=1500)
    instructions = models.TextField(max_length=2500)
    num_ingreds = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.name)

class Ingredient(models.Model):
    CATEGORIES = (
        ('P', 'Protein'),
        ('G', 'Grain'),
        ('F', 'Fruit'),
        ('V', 'Vegetable'),
        ('U', 'Unknown'),
    )

    id = HashidAutoField(primary_key=True, alphabet=HASH_ID_ALPHABET)
    name = models.CharField(max_length=300, unique=True)
    category = models.CharField(max_length=1, choices=CATEGORIES, default='U')

    def __str__(self):
        return str(self.name)
