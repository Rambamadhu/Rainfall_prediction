import streamlit as st
import pickle
import pandas as pd

# Load the trained model and feature names from the pickle file
with open("rainfall_prediction_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
feature_names = model_data["feature_names"]

# Streamlit app title
st.title("Rainfall Prediction App")

# Input fields for user data
st.sidebar.header("Enter Weather Details:")
pressure = st.sidebar.number_input("Pressure", min_value=900.0, max_value=1100.0, step=0.1, value=1015.9)
dewpoint = st.sidebar.number_input("Dew Point", min_value=0.0, max_value=30.0, step=0.1, value=19.9)
humidity = st.sidebar.number_input("Humidity", min_value=0, max_value=100, step=1, value=95)
cloud = st.sidebar.number_input("Cloud Cover", min_value=0, max_value=100, step=1, value=81)
sunshine = st.sidebar.number_input("Sunshine Duration (hours)", min_value=0.0, max_value=15.0, step=0.1, value=0.0)
winddirection = st.sidebar.number_input("Wind Direction", min_value=0.0, max_value=360.0, step=0.1, value=40.0)
windspeed = st.sidebar.number_input("Wind Speed", min_value=0.0, max_value=50.0, step=0.1, value=13.7)

# Predict button
if st.sidebar.button("Predict"):
    # Create input DataFrame
    input_data = pd.DataFrame([[pressure, dewpoint, humidity, cloud, sunshine, winddirection, windspeed]],
                              columns=feature_names)
    # Make prediction
    prediction = model.predict(input_data)
    result = "Rainfall" if prediction[0] == 1 else "No Rainfall"

    # Display prediction result
    st.subheader("Prediction Result:")
    st.write(f"The prediction is: **{result}**")

