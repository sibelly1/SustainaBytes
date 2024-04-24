# save the programm steps in functions 
# first, programm a function to get an user input with streamlit of the available ingredients
# second, programm a function to get an user input with streamlit of the food preferences 
# (the food and preferences data will then be used for the API call that gets the recipe)

#Marti, Mariam, David, (Sibelly) 

#import libraries
import streamlit as st
import apiCall
import matplotlib.pyplot as plt

#Function to check if the food preferences are in the recipes
def recipe_matches_preferences(diet_options:list, recipe_details):

    if recipe_details:
        #Check if a preference was selected
        if 'Vegetarian' in diet_options: 
            if recipe_details["vegetarian"] == False: #We serach in all recipes if they are vegeterian. If not (False), then we skip the recipe 
                return False
        if 'Vegan' in diet_options:
            if recipe_details["vegan"] == False:
                return False
        if 'Dairy Intolerance' in diet_options:
            if recipe_details["dairyFree"] == False:
                return False
        if 'Gluten Free' in diet_options:
            if recipe_details["glutenFree"] == False:
                return False
    
    if len(diet_options) == 0 or 'None' in diet_options: #If no preference is selected the programm continues to run
       return True

    return True


#Website Title
st.title("Sustainabytes")

#Input field for ingredients
ingredients_options = ingredients = ['Eggs', 'Milk', 'Rice', 'Cream cheese', 'Onions', 'Carrots', 'Bell peppers', 'Tomatoes', 'Apples', 'Oranges', 'Lemons', 'Yogurt']
selected_ingredients = st.multiselect('Select Ingredients:', ingredients_options)

#Multiselect for cuisine
cuisine_options = ['African', 'American', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Italian', 'Japanese', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Spanish', 'Thai', 'Vietnamese']
selected_cuisine = st.multiselect('Select Cuisine:', ["All Cuisines"] + cuisine_options)
#code to select all cuisine types when selecitng "All Cuisines"
if "All Cuisines" in selected_cuisine:
    selected_cuisine=cuisine_options

#Multiselect for diet preferences
diet_options = ['Vegetarian','Vegan', 'Dairy Intolerance', 'Gluten Free', 'None']
selected_diet = st.multiselect('Diet preferences:', diet_options)

if st.button('Search Recipes by Ingredients'):
    recipes = apiCall.search_by_ingredients_cuisine(selected_ingredients, selected_cuisine)

# here we check if the recipe details include our diet preferences  

    #Display fetched recipes
    if recipes:
        st.subheader("Here are some recipe suggestions:")
        for recipe in recipes["results"]:

            details = apiCall.fetch_recipe_details(recipe["id"])

            #Check if recipe matches our preferences (function above)
            if recipe_matches_preferences(diet_options, details):

                st.write(f"- {recipe['title']}")
                st.image(recipe['image'])
            # Fetching and displaying recipe details

                if details:
                    st.write("Recipe Details:")
                    st.write(f"Instructions: {details['instructions']}")
                    st.write(f"Servings: {details['servings']}")
                    #getting nutrient info
                    # we could alternatively use the API call from https://spoonacular.com/food-api/docs#Recipe-Nutrition-Label-Widget to get a fancy image of the nutrition info instead of a list
                    nutrients = apiCall.fetch_nutrition_info(recipe['id'])
                    if nutrients:
                        st.write("Nutritional Information:")
                        for nutrient in nutrients['nutrients']:
                            st.write(f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}")
                            #we could create a pie chart with nutri info
    else:
        st.write("No recipes found. Try adjusting your search criteria.")
