#save the programm steps in functions

#Marti, Sibelly

import streamlit as st
import requests
from bs4 import BeautifulSoup #this library was imported to be able to read Nutrients which were displayed in Json format

#Spoonacular API key, needed to access API
#some other keys to use as the free version is limited in it's uses per single key
#7f5e0f00575f483ba2a9ff81371e0a73
#1f0f4ea7e9684b38b3f862e974b37399
#5397833665e64aaf9e8e2bcc02471f85
#f4d2ad2c0486436095b611c765a757f2

API_KEY = "1f0f4ea7e9684b38b3f862e974b37399"

def search_by_ingredients(ingredients):
    url = f'https://api.spoonacular.com/recipes/findByIngredients'
   #Selection of necessary information from the API 
    params = {
        'apiKey': API_KEY,
        'number': 1,  #Number of recipes to fetch, due to free version of API 
        #Depending on the search inputs no recipes might appear, because the 10 recipes do not match the seacrh, but with more recipes it could match
        'ingredients': ingredients,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch recipes by ingredients. Please try again later.")
        return []

def search_by_ingredients_cuisine(ingredients, cuisine):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
   #Selection of necessary information from the API 
    params = {
        'apiKey': API_KEY,
        'number': 10,  #Number of recipes to fetch
        'cuisine': cuisine,
        'includeIngredients': ingredients,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch recipes by ingredients. Please try again later.")
        return []


#Getting recipe details (meaning how to cook the recipe) by recipe ID. An ID is used, as Spoonacular API has an ID for each of their recipes
def fetch_recipe_details(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'instructions' in data:
            instructions_html = data['instructions']
            # Parse HTML instructions to extract text
            soup = BeautifulSoup(instructions_html, 'html.parser')
            instructions_text = ''.join(soup.stripped_strings)  # Extract text content
            data['instructions'] = instructions_text
        return data
    else:
        st.error("Failed to fetch recipe details.")

#Getting nutrition (such as calories) information for a recipe by recipe ID
def fetch_nutrition_info(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch nutrition information.")
