import json
import re
import requests
import os

from extract_ingreds import simplify_ingred

USERNAME = os.environ['APP_USERNAME']
PASSWORD = os.environ['APP_PASSWORD']
RECIPE_URL = 'http://127.0.0.1:8000/data/recipes/?format=json'
INGRED_URL = 'http://127.0.0.1:8000/data/ingredients/'

def post_recipe(name, ingred_list, simple_ingred_list, instructions, num_ingreds):
    data = {
        'name': name,
        'ingred_list': ingred_list,
        'simple_ingred_list': simple_ingred_list,
        'instructions': instructions,
        'num_ingreds': num_ingreds
    }
    return requests.post(RECIPE_URL, json=data, auth=(USERNAME, PASSWORD))

def post_ingred(name, category=''):
    data = {
        'name': name,
    }
    if category != '':
        data['category'] = category
    return requests.post(INGRED_URL, json=data, auth=(USERNAME, PASSWORD))

def get_ingred_id(name):
    return requests.get(INGRED_URL + '?name=' + name).json()[0]['id']

with open('recipes_raw_nosource_ar.json', 'r') as read_file:
    data = json.load(read_file)
    test_size = 10 # max number of recipes to post, remove to post all
    recipes_posted = 0 # remove to post all
    for recipe in data.values():
        ingred_list = ''
        simple_ingred_list = ''
        num_ingreds = 0
        try:
            for ingred in recipe['ingredients']:
                ingred = re.sub(r'ADVERTISEMENT', '', ingred)
                if ingred == '':
                    continue
                ingred_list += ingred + '\n'
                simple_ingred = simplify_ingred(ingred)
                if simple_ingred != '':
                    response = post_ingred(simple_ingred).json()
                    if 'id' not in response:
                        simple_ingred_list += get_ingred_id(simple_ingred) + '\n'
                    else:
                        simple_ingred_list += response['id'] + '\n'
                num_ingreds += 1
            if ingred_list == '':
                continue
            post_recipe(recipe['title'], ingred_list, simple_ingred_list, recipe['instructions'], num_ingreds)
            recipes_posted += 1 # remove to post all
            if recipes_posted == test_size: # remove to post all
                break # remove to post all
        except KeyError:
            continue