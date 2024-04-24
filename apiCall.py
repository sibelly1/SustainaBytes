#save the programm steps in functions
#make the api call to show only the relevant recipes

#Marti, Alexandra, Lou, Sibelly

import streamlit as st
import requests
from bs4 import BeautifulSoup #this library was imported to be able to read Nutrients which were displayed in Json format

#Spoonacular API key, needed to access API
API_KEY = "1f0f4ea7e9684b38b3f862e974b37399"

def search_by_ingredients(ingredients):
    url = f'https://api.spoonacular.com/recipes/findByIngredients'
   #Selection of necessary information from the API 
    params = {
        'apiKey': API_KEY,
        'number': 20,  #Number of recipes to fetch, due to free version of API 
        #Depending on the search inputs no recipes might appear, because the 20 recipes do not match the seacrh, but with more recipes it could match
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
        'number': 20,  #Number of recipes to fetch
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
        return response.json()
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
