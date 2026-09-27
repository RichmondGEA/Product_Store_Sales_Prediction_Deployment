
import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# Create the directory if it doesn't exist
output_dir = "backend_files"
os.makedirs(output_dir, exist_ok=True)
output_filepath = os.path.join(output_dir, "app.py")

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("Product_Store_Sales_prediction_model_v1_0.joblib")

model = load_model()

# Streamlit UI for Price Prediction
st.title("Product Store Sales Prediction App")
st.write("This tool predicts predicts thetotal sales of products based on its location")

st.subheader("Enter the listing details:")
app_content = """


# Initialize Flask app with a name
Product_Sales_Predictor_api = Flask("Product Store Sales Predictor")

# Load the trained sales prediction model
# The model file is assumed to be in 'deployment_files/' relative to the container's /app directory
# Corrected path assuming app.py is in /app/backend_files/ and model is in /app/deployment_files/
model_path = "../deployment_files/Product_Store_Sales_prediction_model_v1_0.joblib"
model = joblib.load(model_path)

# Define a route for the home page
@Product_Sales_Predictor_api.get('/')
def home():
    return "Welcome to the Product Store Sales Total Prediction API!"

# Define an endpoint to predict sales for a single store
@Product_Sales_Predictor_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    input_json_data = request.get_json()

    # Extract relevant features from the input data
    sample = {
        'Product_Weight': input_json_data['Product_Weight'],
        'Product_Allocated_Area': input_json_data['Product_Allocated_Area'],
        'Product_MRP': input_json_data['Product_MRP'],
        'Store_Establishment_Year': input_json_data['Store_Establishment_Year'],
        'Product_Sugar_Content': input_json_data['Product_Sugar_Content'],
        'Product_Type': input_json_data['Product_Type'],
        'Store_Size': input_json_data['Store_Size'],
        'Store_Location_City_Type': input_json_data['Store_Location_City_Type'],
        'Store_Type': input_json_data['Store_Type']
    }

    # Convert the extracted data into a DataFrame
    input_df = pd.DataFrame([sample])

    # Make a sales prediction using the trained model
    prediction = model.predict(input_df).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Prediction': prediction})

# Define an endpoint to predict sales for a batch of products/stores
@Product_Sales_Predictor_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    # Assuming Product_Id is the identifier column to drop for prediction, but kept for output mapping.
    # The model is a regression model, so raw numerical predictions are returned.
    if "Product_Id" in input_data.columns:
        features_for_prediction = input_data.drop("Product_Id", axis=1)
        product_id_list = input_data.Product_Id.values.tolist()
    else:
        features_for_prediction = input_data
        product_id_list = [f"item_{i}" for i in range(len(input_data))]

    predictions = model.predict(features_for_prediction).tolist()

    output_dict = dict(zip(product_id_list, predictions))

    return jsonify(output_dict)

# Run the Flask app in debug mode
if __name__ == '__main__':
    Product_Sales_Predictor_api.run(debug=True, host='0.0.0.0', port=7860)
"""

with open(output_filepath, "w") as f:
    f.write(app_content)

print(f"File '{output_filepath}' created successfully.")
