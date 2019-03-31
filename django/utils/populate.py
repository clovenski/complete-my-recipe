import json
import re
import os

def generate_recipes_json():
    if not os.path.exists('../api/completemyrecipe/fixtures/'):
        os.mkdir('../api/completemyrecipe/fixtures/')
    with open('../api/completemyrecipe/fixtures/recipes.json', 'w') as out_file:
        recipes_json = []
        with open('recipes_raw_nosource_ar.json', 'r') as read_file:
            data = json.load(read_file)
            # test_size = 5 # max number of recipes to post, remove to post all
            recipe_num = 1
            for recipe in data.values():
                ingred_list = ''
                num_ingreds = 0
                try:
                    for ingred in recipe['ingredients']:
                        ingred = re.sub(r'ADVERTISEMENT', '', ingred)
                        if ingred == '':
                            continue
                        ingred_list += ingred + '\n'
                        num_ingreds += 1
                    if ingred_list == '':
                        continue
                    ingred_list = ingred_list[:-2]
                    recipes_json.append({
                        'model': 'completemyrecipe.Recipe',
                        'pk': recipe_num,
                        'fields': {
                            'name': recipe['title'],
                            'ingred_list': ingred_list,
                            'instructions': recipe['instructions'],
                            'num_ingreds': num_ingreds
                        }
                    })
                    recipe_num += 1
                    # if recipe_num > test_size: # remove to post all
                    #     break # remove to post all
                except KeyError:
                    continue
        json.dump(recipes_json, out_file, indent=2)

def generate_ingreds_json():
    if not os.path.exists('../api/completemyrecipe/fixtures/'):
        os.mkdir('../api/completemyrecipe/fixtures/')
    with open('../api/completemyrecipe/fixtures/ingreds.json', 'w') as out_file:
        ingreds_json = []
        ingred_num = 1
        # example ingredient data, used for testing
        ingreds_json.append({
            'model': 'completemyrecipe.Ingredient',
            'pk': ingred_num,
            'fields': {
                'name': 'chicken',
                'category': 'P'
            }
        })
        ingred_num += 1
        ingreds_json.append({
            'model': 'completemyrecipe.Ingredient',
            'pk': ingred_num,
            'fields': {
                'name': 'beef',
                'category': 'P'
            }
        })
        ingred_num += 1
        ingreds_json.append({
            'model': 'completemyrecipe.Ingredient',
            'pk': ingred_num,
            'fields': {
                'name': 'rice',
                'category': 'G'
            }
        })
        ingred_num += 1
        ingreds_json.append({
            'model': 'completemyrecipe.Ingredient',
            'pk': ingred_num,
            'fields': {
                'name': 'apple',
                'category': 'F'
            }
        })
        json.dump(ingreds_json, out_file, indent=2)

if __name__ == '__main__':
    generate_recipes_json()
    generate_ingreds_json()