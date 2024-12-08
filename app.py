import streamlit as st
import pickle
import pandas as pd

# Load the trained model and feature names from the pickle file
with open("rainfall_prediction_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
feature_names = model_data["feature_names"]

# Custom CSS and JavaScript for falling rain animation
rain_animation = """
<style>
body {
    margin: 0;
    overflow: hidden;
    background: linear-gradient(to bottom, #2c3e50, #2980b9);
}

#rain-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
}
</style>
<canvas id="rain-canvas"></canvas>
<script>
const canvas = document.getElementById("rain-canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let raindrops = [];

function createRaindrop() {
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        speed: Math.random() * 5 + 2,
        length: Math.random() * 20 + 10,
    };
}

function updateRaindrops() {
    raindrops.forEach((drop) => {
        drop.y += drop.speed;
        if (drop.y > canvas.height) {
            drop.y = -drop.length;
            drop.x = Math.random() * canvas.width;
        }
    });
}

function drawRaindrops() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
    ctx.lineWidth = 1.5;
    raindrops.forEach((drop) => {
        ctx.beginPath();
        ctx.moveTo(drop.x, drop.y);
        ctx.lineTo(drop.x, drop.y + drop.length);
        ctx.stroke();
    });
}

function loop() {
    updateRaindrops();
    drawRaindrops();
    requestAnimationFrame(loop);
}

for (let i = 0; i < 500; i++) {
    raindrops.push(createRaindrop());
}

loop();

window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>
"""

# Streamlit App UI
st.set_page_config(page_title="Rainfall Prediction", layout="wide")

st.markdown(
    """
    <h1 style="color: white; text-align: center;">🌦️ Rainfall Prediction Application</h1>
    <p style="color: white; text-align: center;">
    Enter the weather details below, and we'll predict whether it will rain!
    </p>
    """,
    unsafe_allow_html=True,
)

# Input fields
st.sidebar.header("Enter Weather Details")
inputs = {}
for feature in feature_names:
    inputs[feature] = st.sidebar.number_input(f"Enter {feature}", value=0.0)

# Make prediction
input_df = pd.DataFrame([inputs.values()], columns=feature_names)
prediction = model.predict(input_df)[0]

# Display result and animation if rainfall
if prediction == 1:
    st.markdown(
        "<h2 style='color: white; text-align: center;'>🌧️ It is likely to Rain!</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(rain_animation, unsafe_allow_html=True)
else:
    st.markdown(
        "<h2 style='color: white; text-align: center;'>☀️ No Rainfall expected.</h2>",
        unsafe_allow_html=True,
    )
