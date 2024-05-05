#Marti, Sibelly

# --- Import libraries ---
import streamlit as st
import apiCall
import matplotlib.pyplot as plt

# --- Function to check if the food preferences are in the recipes ---
def recipe_matches_preferences(diet_options:list, recipe_details):

    if recipe_details:
        # Check if a preference was selected
        if 'Vegetarian' in diet_options: 
            if recipe_details["vegetarian"] == False: # We serach in all recipes if they are vegeterian. If not (False), then we skip the recipe 
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
    
    if len(diet_options) == 0 or 'None' in diet_options: # If no preference is selected the programm continues to run
       return True

    return True


#--- Website App Title & Description ---
st.set_page_config(page_title="SustainaBytes", page_icon="🥗")
st.title("SustainaBytes")
st.write("Find delicious recipes with the ingredients you have at home and help reduce food waste!")


# --- User inputs ---
# Input field for ingredients
ingredients_options = ingredients = ['Chicken', 'Tomato', 'Onion', 'Potato', 'Pasta','Pepper', 'Eggs', 'Milk', 'Rice','Cream cheese', 'Carrots']
selected_ingredients = st.multiselect('Select Ingredients:', ingredients_options)

# Multiselect for cuisine
cuisine_options = ['African', 'American', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Italian', 'Japanese', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Spanish', 'Thai', 'Vietnamese']
selected_cuisine = st.multiselect('Select Cuisine:', ["All Cuisines"] + cuisine_options)
#code to select all cuisine types when selecitng "All Cuisines"
if "All Cuisines" in selected_cuisine:
    selected_cuisine=cuisine_options

# Multiselect for diet preferences
diet_options = ['Vegetarian','Vegan', 'Dairy Intolerance', 'Gluten Free', 'None']
selected_diet = st.multiselect('Diet preferences:', diet_options)


# --- Fetch & Display Recipes ---
if st.button(' 🔍 Find Recipes'):
    recipes = apiCall.search_by_ingredients_cuisine(selected_ingredients, selected_cuisine)

    if recipes:
        st.subheader("Here are some recipe suggestions:")
        
        # Display recipes in two columns
        col1, col2 = st.columns(2)

        # Counter for alternating between columns
        col_counter = 0

        for recipe in recipes["results"]:
            details = apiCall.fetch_recipe_details(recipe["id"])

            # Check if recipe matches our preferences (function above)
            if recipe_matches_preferences(diet_options, details):
                recipe_name = recipe['title']
                recipe_id = recipe['id']
                recipe_link = f"https://spoonacular.com/recipes/{recipe_id}"

                if col_counter % 2 == 0:
                    with col1:
                        # Display recipe name as a clickable link
                        st.write(f"### [{recipe_name}]({recipe_link})")
                        st.image(recipe['image'], use_column_width=True)
                        
                        # Fetching and displaying recipe details
                        if details:
                            st.write(f"Servings: {details['servings']}")
                            # Fetch nutrient information
                            nutrients = apiCall.fetch_nutrition_info(recipe['id'])
                            if nutrients:
                                nutrient_names = []
                                nutrient_values = []
                                for nutrient in nutrients['nutrients']:
                                    nutrient_names.append(nutrient['name'])
                                    nutrient_values.append(nutrient['amount'])
                
                else:
                    with col2:
                        # Display recipe name as a clickable link
                        st.write(f"### [{recipe_name}]({recipe_link})")
                        st.image(recipe['image'], use_column_width=True)
                        if details:
                            st.write(f"Servings: {details['servings']}")
                            # Fetch nutrient information
                            nutrients = apiCall.fetch_nutrition_info(recipe['id'])
                            if nutrients:
                                nutrient_names = []
                                nutrient_values = []
                                for nutrient in nutrients['nutrients']:
                                    nutrient_names.append(nutrient['name'])
                                    nutrient_values.append(nutrient['amount'])

                col_counter += 1

            # Display pie chart for some nutrients
                if nutrients:
                    st.write("Pie Chart of Nutrients:")
                    fig, ax = plt.subplots()
                    ax.pie(nutrient_values[:8], labels=nutrient_names[:8], autopct='%1.1f%%') # We only display a pie chart for the first 8 nutrients in the list (can be adjusted)
                    st.pyplot(fig)

        else:
            st.write("No recipes found. Try adjusting your search criteria.")
