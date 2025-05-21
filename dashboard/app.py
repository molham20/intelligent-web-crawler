import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="TasteOfHome Recipes", page_icon="🍲", layout="wide")

# Load recipe data
def load_recipe_data():
    try:
        with open("recipe_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Recipe data file not found. Please run the scraper first.")
        return None
    except json.JSONDecodeError:
        st.error("Error reading recipe data. File might be corrupted.")
        return None

# Main app
def main():
    st.title("🍲 TasteOfHome Recipe Explorer")
    st.markdown("Explore scraped recipes with ingredients and preparation steps")
    
    recipe_data = load_recipe_data()
    if not recipe_data:
        return
    
    # Display basic info in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Recipe Name", recipe_data['title'])
    with col2:
        st.metric("Ingredients Count", len(recipe_data['ingredients']))
    with col3:
        st.metric("Steps Count", len(recipe_data['directions']))
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 Ingredients", "👨‍🍳 Directions", "📊 Analysis"])
    
    with tab1:
        st.subheader("Ingredients List")
        for i, ingredient in enumerate(recipe_data['ingredients'], 1):
            st.markdown(f"- {ingredient}")
    
    with tab2:
        st.subheader("Cooking Directions")
        for i, step in enumerate(recipe_data['directions'], 1):
            st.markdown(f"{i}. {step}")
    
    with tab3:
        st.subheader("Recipe Analysis")
        
        # Create a DataFrame for visualization
        df = pd.DataFrame({
            'Category': ['Ingredients', 'Steps'],
            'Count': [len(recipe_data['ingredients']), len(recipe_data['directions'])]
        })
        
        st.bar_chart(df.set_index('Category'))
        
        # Time estimates if available
        if recipe_data.get('prep_time') != "غير متوفر" or recipe_data.get('cook_time') != "غير متوفر":
            st.subheader("Time Estimates")
            col1, col2 = st.columns(2)
            if recipe_data.get('prep_time') != "غير متوفر":
                col1.metric("Preparation Time", recipe_data['prep_time'])
            if recipe_data.get('cook_time') != "غير متوفر":
                col2.metric("Cooking Time", recipe_data['cook_time'])

if __name__ == "__main__":
    main()