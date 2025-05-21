import streamlit as st
import pandas as pd

st.title("🚀 TasteOfHome Web Crawler Dashboard")

# عرض بيانات الوصفات
recipes = pd.read_csv("recipe_data.json")
st.dataframe(recipes.head())

# رسم بياني
st.bar_chart(recipes["cooking_time"].value_counts())