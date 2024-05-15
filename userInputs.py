# --- Import libraries ---
import streamlit as st
import apiCall
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup #this library was imported to be able to read Nutrients which were displayed in Json format

# --- Function to check if recipe matches the user's dietary preferences ---
def recipe_matches_preferences(diet_options:list, recipe_details):
    if recipe_details:
        # Check if a preference was selected
        if 'Vegetarian' in diet_options: 
            if recipe_details["vegetarian"] == False: # We serach in all recipes if they are vegeterian. If not (False), then we skip the recipe 
                return False
        if 'Vegan' in diet_options:
            if recipe_details["vegan"] == False: # Check if recipe is vegan
                return False
        if 'Dairy Intolerance' in diet_options:
            if recipe_details["dairyFree"] == False: # Check if recipe is dairy-free
                return False
        if 'Gluten Free' in diet_options:
            if recipe_details["glutenFree"] == False: # Check if recipe is gluten-free
                return False
    
    if len(diet_options) == 0 or 'None' in diet_options: # If no preference is selected the programm continues to run
       return True

    return True


#--- Website App Title & Description ---
st.set_page_config(page_title="SustainaBytes", page_icon="🥗") # Set page title and icon
st.title("SustainaBytes") # Displaying the title
st.write("Find delicious recipes with the ingredients you have at home and help reduce food waste!") # Displaying description


# --- User inputs ---
# Input field for ingredients
ingredients_options = ingredients = ['Chicken', 'Tomato', 'Onion', 'Potato', 'Pasta','Pepper', 'Eggs', 'Milk', 'Rice','Cream cheese', 'Carrots']
selected_ingredients = st.multiselect('Select Ingredients:', ingredients_options)

# Multiselect for cuisine
cuisine_options = ['African', 'American', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Italian', 'Japanese', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Spanish', 'Thai', 'Vietnamese']
selected_cuisine = st.multiselect('Select Cuisine:', cuisine_options)

# Multiselect for diet preferences
diet_options = ['Vegetarian','Vegan', 'Dairy Intolerance', 'Gluten Free']
selected_diet = st.multiselect('Diet preferences:', diet_options)


# --- Fetch & Display Recipes ---
if st.button(' 🔍 Find Recipes'):
    # Fetch recipes based on selected ingredients and cuisine
    recipes = apiCall.search_by_ingredients_cuisine(selected_ingredients, selected_cuisine) 

    if recipes:
        # Displaying subheader for recipe suggestions
        st.subheader("Here are some recipe suggestions:") 

        for recipe in recipes["results"]:
            #Fetch details of each recipe
            details = apiCall.fetch_recipe_details(recipe["id"])

            # Checking if the recipe matches dietary preferences with the function above
            if recipe_matches_preferences(selected_diet, details):  
                recipe_name = recipe['title']
                recipe_id = recipe['id']
                
                #Display recipe name in a larger font size & image
                st.write(f"### {recipe_name}")
                st.image(recipe['image'])
                
                #Display details
                if details:
                    st.write(f"Servings: {details['servings']}")
                    st.write("Recipe Instructions:")
                    st.write(details['instructions'])
    
                # --- Displaying DATA nutrient information through a pie chart ---
                nutrients = apiCall.fetch_nutrition_info(recipe['id']) # Fetch nutrient information
                if nutrients:
    # Filtering out 'Calories' nutrient as it posed a problem in the pie chart, 
    # when calories appeared, the pie chart didn't have enough space to show the other more important nutrients (as calories took arount 95% of the space)
    # Furthermore, calories aren't a nutrient and that is why we filter it out
                    nutrients_filtered = [nutrient for nutrient in nutrients['nutrients'] if nutrient['name'] != 'Calories']
    
    # Extracting nutrient names and values per serving, as the pie chart will show the nutrients per serving
                    nutrient_names = [nutrient['name'] for nutrient in nutrients_filtered]
                    #here we add +0.001, as some issue arrises where the pie chart can't be shown as it isn't divisible by 0
                    nutrient_values_per_serving = [nutrient['amount'] / (nutrient['percentOfDailyNeeds']+0.001) for nutrient in nutrients_filtered]
                    nutrient_units = [nutrient['unit'] for nutrient in nutrients_filtered]

    # Calculate the total nutrient amount per serving
                    total_nutrient_per_serving = sum(nutrient_values_per_serving)

                    # The following section was written with the help of Chatgpt 
                    st.write("Pie Chart of Nutrients per serving (without Calories)")
                    fig, ax = plt.subplots()
                    #This line creates a pie chart with Matplotlib and then plots the nutrient amounts (without calories) in grams in the pie chart
                    #it also gives a percentage of the nutrients alongside the gram amounts. All of this with the name of the nutrient
                    #ChatGPT helped with next line of code with prompt "Visualize the distribution of the top six nutrient values per serving using a pie chart. Ensure that the labels correspond to the nutrient names, and each segment of the pie displays the percentage and absolute value of the respective nutrient, formatted with one decimal point precision."
                    ax.pie(nutrient_values_per_serving[:6], labels=nutrient_names[:6], autopct=lambda pct: f"{pct:.1f}% ({pct/100*total_nutrient_per_serving:.1f}{nutrient_units[:6][int(pct / 100. * len(nutrient_units[:6]))]})")
                    st.pyplot(fig)#Display 
            
    else:
        st.write("We couldn't find recipes with these criteria :/")
