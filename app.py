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

# CSS for raindrop animation
raindrop_animation = """
<style>
@keyframes raindrop {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(500px); opacity: 0; }
}

.raindrop {
    position: absolute;
    top: -50px;
    width: 5px;
    height: 15px;
    background: rgba(0, 0, 255, 0.5);
    animation: raindrop 2s linear infinite;
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

</style>
<div id="rain-container"></div>
<script>
for (let i = 0; i < 100; i++) {
    let raindrop = document.createElement("div");
    raindrop.className = "raindrop";
    raindrop.style.left = Math.random() * window.innerWidth + "px";
    raindrop.style.animationDuration = Math.random() * 2 + 1 + "s";
    document.getElementById("rain-container").appendChild(raindrop);
}
</script>
"""

# Display raindrop animation if rainfall is predicted
def show_rain_animation():
    st.markdown(raindrop_animation, unsafe_allow_html=True)

# App header
st.title("🌦️ Rainfall Prediction Application")
st.markdown("""
Welcome to the **Rainfall Prediction App**!  
Enter the weather details on the left sidebar, and this app will predict whether it will rain or not 🌧️☀️.
""")

# Sidebar inputs
st.sidebar.header("Enter Weather Details:")
pressure = st.sidebar.number_input("Pressure (hPa)", min_value=900.0, max_value=1100.0, step=0.1, value=1015.9)
dewpoint = st.sidebar.number_input("Dew Point (°C)", min_value=0.0, max_value=30.0, step=0.1, value=19.9)
humidity = st.sidebar.number_input("Humidity (%)", min_value=0, max_value=100, step=1, value=95)
cloud = st.sidebar.number_input("Cloud Cover (%)", min_value=0, max_value=100, step=1, value=81)
sunshine = st.sidebar.number_input("Sunshine Duration (hours)", min_value=0.0, max_value=15.0, step=0.1, value=0.0)
winddirection = st.sidebar.number_input("Wind Direction (degrees)", min_value=0.0, max_value=360.0, step=0.1, value=40.0)
windspeed = st.sidebar.number_input("Wind Speed (km/h)", min_value=0.0, max_value=50.0, step=0.1, value=13.7)

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
    if prediction[0] == 1:
        st.success("🌧️ It is likely to Rain!")
        show_rain_animation()  # Show raindrop animation
    else:
        st.info("☀️ No Rainfall expected.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io) | 🌦️ Rainfall Prediction App")
