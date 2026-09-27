import requests
import streamlit as st
import pandas as pd

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"


st.title("Product Store Sales Prediction")

# Online Prediction
st.subheader("Online Prediction")

# Input fields for product and store data
Store_Id = st.text_input("Store ID (e.g., OUT001)", value="OUT001") # Changed to text_input as Store_Id seems to be object type
Product_Weight = st.number_input("Product Weight", min_value=1.0, max_value=100.0, value=12.66)
Product_Allocated_Area = st.number_input("Product Allocated Area (ratio)", min_value=0.001, max_value=0.3, value=0.027, format="%.3f") # Adjusted max and format for ratio
Product_MRP = st.number_input("Product MRP (Maximum Retail Price)", min_value=1.0, max_value=300.0, value=117.08)
Store_Establishment_Year = st.number_input("Store Establishment Year", min_value=1980, max_value=2024, value=2009)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
Product_Type = st.selectbox("Product Type", ['Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 'Snack Foods', 'Fruits and Vegetables', 'Household', 'Meat', 'Soft Drinks', 'Breads', 'Hard Drinks', 'Others', 'Starchy Foods', 'Breakfast', 'Seafood'])
Store_Size = st.selectbox("Store Size", ["Medium", "High", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type2", "Departmental Store", "Supermarket Type1", "Food Mart"])

store_data = {
    'Product_Weight': Product_Weight,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Establishment_Year': int(Store_Establishment_Year),
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Type': Product_Type,
    'Store_Id': Store_Id,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type
}


if st.button("Predict Sales", type='primary'):
    # Make sure to replace <user_name>-<space_name> with your actual Hugging Face Space URL
    response = requests.post("https://<user_name>-<space_name>.hf.space/v1/store", json=store_data) # Changed endpoint to /v1/store
    if response.status_code == 200:
        result = response.json()
        sales_prediction = result["Prediction"] # Changed variable name to sales_prediction
        st.write(f"Predicted Sales for Product in Store {Store_Id}: {sales_prediction:.2f}") # Updated message and format
    else:
        st.error(f"Error in API request: {response.status_code} - {response.text}")

# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None:
    if st.button("Predict Sales for Batch", type='primary'): # Changed button text
        # Make sure to replace <user_name>-<space_name> with your actual Hugging Face Space URL
        response = requests.post("https://<user_name>-<space_name>.hf.space/v1/storebatch", files={"file": file}) # Changed endpoint to /v1/storebatch
        if response.status_code == 200:
            result = response.json()
            st.header("Batch Sales Prediction Results") # Changed header
            st.write(result)
        else:
            st.error(f"Error in API request: {response.status_code} - {response.text}")
