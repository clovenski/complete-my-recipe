import json
import re

REMOVE_PATTERNS = [
    r'\d*',
    r',',
    r'-+',
    r'/',
    r'\(.*\)',
    r'.*:',
    u'\u2122',
    r'\.+',
    u'\u00ae',
    r'\%',
    r'®',
    r'\*',
]

REMOVE_PAT_WORDS = [
    r'\W?ounces?',
    r'\W?pounds?',
    r'\W?cans?',
    r'\W?cups?',
    r'\W?teaspoons?',
    r'\W?tablespoons?',
    r'\W?cloves?',
    r'\W?packages?',
    r'\W?cartons?',
    r'\W?gallons?',
    r'\W?pints?',
    r'\W?pieces?',
]

REMOVE_WORDS = [
    'advertisement',
    'pinch',
    'packed',
    'skinless',
    'boneless',
    'halves',
    'finely',
    'diced',
    'dice',
    'sliced',
    'cubed',
    'and',
    'reduced',
    'fat',
    'ground',
    'refrigerated',
    'torn',
    'into',
    'chopped',
    'all-purpose',
    'semisweet',
    'softened',
    'fresh',
    'freshly',
    'medium',
    'large',
    'extralong',
    'minced',
    'divided',
    'shredded',
    'fine',
    'beaten',
    'mashed',
    'to',
    'taste',
    'juiced',
    'or',
    'cleaned',
    'cracked',
    'cooked',
    'uncooked',
    'more',
    'as',
    'needed',
    'with',
    'chives',
    'oz',
    'inch',
    'lightly',
    'thin',
    'thinly',
    'slice',
    'of',
    'cubes',
    'fluid',
    'pkg',
    'in',
    'pint',
    'crushed',
    'removed',
    'but',
    'not',
    'peeled',
    'tub',
    'seeded',
    'stems',
    'intact',
    'halved',
]

# function to be used by populate.py
def simplify_ingred(ingred):
    for pattern in REMOVE_PATTERNS:
        ingred = re.sub(pattern, '', ingred).strip()
    for pattern in REMOVE_PAT_WORDS:
        ingred = re.sub(pattern, ' ', ingred).strip()
    ingred = re.sub(r'\s+', ' ', ingred).strip()
    ingred = ingred.split()
    ingredient = ''
    for i in ingred:
        if i.lower() not in REMOVE_WORDS:
            ingredient += i + ' '
    return ingredient.strip()

## code that was used to examine what kind of processing was done to ingredient strings
# read_file = open('recipes_raw_nosource_ar.json', 'r')
# data = json.load(read_file)
# # test_size = 100
# ingredients = set([])
# ingred_printed = 0
# for recipe in data.values():
#     try:
#         for ingred in recipe['ingredients']:
#             ingredient = simplify_ingred(ingred)
#             if ingredient != '':
#                 ingredients.add(ingredient)
#         # if ingred_printed >= test_size:
#         #     break
#     except KeyError:
#         continue

# print(len(ingredients))
# write_file = open('ingredients.txt', 'w+', encoding='utf-8')
# for ingredient in ingredients:
#     write_file.write(ingredient + '\n')
