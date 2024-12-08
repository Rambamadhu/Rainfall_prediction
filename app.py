import streamlit as st
import pickle
import pandas as pd

# Load the trained model and feature names from the pickle file
with open("rainfall_prediction_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
feature_names = model_data["feature_names"]

# Set the app title and layout
st.set_page_config(page_title="Rainfall Prediction App", page_icon="🌧️", layout="wide")

# HTML and CSS for raindrop background animation
rain_animation = """
<style>
body {
    margin: 0;
    padding: 0;
    background: linear-gradient(to bottom, #1e3c72, #2a5298);
    overflow: hidden;
}

#rain-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
}

.raindrop {
    position: absolute;
    top: -10px;
    width: 2px;
    height: 30px;
    background: rgba(255, 255, 255, 0.6);
    animation: fall 2s infinite;
    animation-timing-function: linear;
}

@keyframes fall {
    to {
        transform: translateY(100vh);
    }
}

</style>
<div id="rain-container"></div>
<script>
const rainContainer = document.getElementById('rain-container');

function createRaindrop() {
    const raindrop = document.createElement('div');
    raindrop.classList.add('raindrop');
    raindrop.style.left = Math.random() * window.innerWidth + 'px';
    raindrop.style.animationDuration = Math.random() * 2 + 2 + 's';
    rainContainer.appendChild(raindrop);

    setTimeout(() => {
        rainContainer.removeChild(raindrop);
    }, 4000);
}

setInterval(createRaindrop, 100);
</script>
"""

# Add the rain animation to the app
st.markdown(rain_animation, unsafe_allow_html=True)

# App header
st.title("🌦️ Rainfall Prediction Application")
st.markdown("""
Welcome to the **Rainfall Prediction App**!  
Enter the weather details below, and the app will predict whether it will rain or not 🌧️☀️.
""")

# Input form
st.header("Enter Weather Details")
with st.form("weather_form"):
    pressure = st.number_input("Pressure (hPa)", min_value=900.0, max_value=1100.0, step=0.1, value=1015.9)
    dewpoint = st.number_input("Dew Point (°C)", min_value=0.0, max_value=30.0, step=0.1, value=19.9)
    humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, step=1, value=95)
    cloud = st.number_input("Cloud Cover (%)", min_value=0, max_value=100, step=1, value=81)
    sunshine = st.number_input("Sunshine Duration (hours)", min_value=0.0, max_value=15.0, step=0.1, value=0.0)
    winddirection = st.number_input("Wind Direction (degrees)", min_value=0.0, max_value=360.0, step=0.1, value=40.0)
    windspeed = st.number_input("Wind Speed (km/h)", min_value=0.0, max_value=50.0, step=0.1, value=13.7)
    
    # Submit button
    submitted = st.form_submit_button("Predict")

# Prediction
if submitted:
    # Create input DataFrame
    input_data = pd.DataFrame([[pressure, dewpoint, humidity, cloud, sunshine, winddirection, windspeed]],
                              columns=feature_names)
    # Make prediction
    prediction = model.predict(input_data)
    result = "Rainfall" if prediction[0] == 1 else "No Rainfall"

    # Display prediction result
    st.subheader("Prediction Result:")
    if prediction[0] == 1:
        st.success("🌧️ It is likely to Rain!")
    else:
        st.info("☀️ No Rainfall expected.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io) | 🌦️ Rainfall Prediction App")
