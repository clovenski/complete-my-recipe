import json
import re
import requests
import os

USERNAME = os.environ['APP_USERNAME']
PASSWORD = os.environ['APP_PASSWORD']
POST_URL = 'http://127.0.0.1:8000/data/recipes/?format=json'

def post_recipe(name, ingred_list, instructions, num_ingreds):
    data = {
        'name': name,
        'ingred_list': ingred_list,
        'instructions': instructions,
        'num_ingreds': num_ingreds
    }
    requests.post(POST_URL, json=data, auth=(USERNAME, PASSWORD))

with open('recipes_raw_nosource_ar.json', 'r') as read_file:
    data = json.load(read_file)
    test_size = 5 # max number of recipes to post, remove to post all
    recipes_posted = 0 # remove to post all
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
            post_recipe(recipe['title'], ingred_list, recipe['instructions'], num_ingreds)
            recipes_posted += 1 # remove to post all
            if recipes_posted == test_size: # remove to post all
                break # remove to post all
        except KeyError:
            continue