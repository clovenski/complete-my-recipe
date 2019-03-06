import json
import requests

url = 'http://127.0.0.1:8000/recipes/'

def post_recipe(name, ingred_list, instructions, num_ingreds):
    data = {
        'name': name,
        'ingred_list': ingred_list,
        'instructions': instructions,
        'num_ingreds': num_ingreds
    }
    requests.post(url, json=data)

with open('recipes_raw_nosource_ar.json', 'r') as read_file:
    data = json.load(read_file)
    print(data["rmK12Uau.ntP510KeImX506H6Mr6jTu"]['title']) # this prints Slow Cooker Chicken and Dumplings
    # for recipe in data.values():
        # convert json format in dataset to format in post_recipe method
        # then call post_recipe to post into database, assuming server is running