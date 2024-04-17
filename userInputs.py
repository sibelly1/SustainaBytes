# save the programm steps in functions 
# first, programm a function to get an user input with streamlit of the available ingredients
# second, programm a function to get an user input with streamlit of the food preferences 
# (the food and preferences data will then be used for the API call that gets the recipe)

#Marti, Mariam, David, (Sibelly) 

#import libraries
import streamlit as st
import apiCall


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

#Multiselect for intolerance and putting all at the end
intolerance_options = ['Dairy', 'Egg', 'Gluten', 'Grain', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy',]
selected_intolerance = st.multiselect('Select Intolerance:', intolerance_options + ["All Intolerances"])
#same code as above to select all intolerances
if "All Intolerances" in intolerance_options:
    selected_intolerance=intolerance_options

#Multiselect for diet
diet_options = ['Gluten Free', 'Ketogenic', 'Vegetarian', 'Lacto-Vegetarian', 'Vegan', 'Pescetarian']
selected_diet = st.multiselect('Select Diet:', diet_options)

if st.button('Search Recipes by Ingredients'):
    recipes = apiCall.search_by_ingredients(selected_ingredients)

    #Display fetched recipes
    if recipes:
        st.subheader("Here are some recipe suggestions:")
        for recipe in recipes:
            st.write(f"- {recipe['title']}")
    else:
        st.write("No recipes found. Try adjusting your search criteria.")
