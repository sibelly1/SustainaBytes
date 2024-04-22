#save the programm steps in functions
#make the api call to show only the relevant recipes

#Marti, Alexandra, Lou, Sibelly

import streamlit as st
import requests
from bs4 import BeautifulSoup #this library was imported to be able to read Nutrients which were displayed in Json format

#Spoonacular API key, needed to access API
API_KEY = "7f5e0f00575f483ba2a9ff81371e0a73"


def search_by_selection(ingredients, cuisine, intolerances, diets):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
   #Selection of necessary information from the API 
    params = {
        'apiKey': API_KEY,
        'number': 20,  #Number of recipes to fetch
        'ingredients': ingredients,
        'cuisine': cuisine,
        'intolerances': intolerances,
        'diets': diets
    }

    print(params)

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch recipes. Please try again later.")
        return []    

def search_by_ingredients(ingredients):
    url = f'https://api.spoonacular.com/recipes/findByIngredients'
   #Selection of necessary information from the API 
    params = {
        'apiKey': API_KEY,
        'number': 20,  #Number of recipes to fetch
        'ingredients': ingredients,
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
