import streamlit as st
import pickle
import pandas as pd

# Load the trained model and feature names from the pickle file
with open("rainfall_prediction_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
feature_names = model_data["feature_names"]

# Improved CSS and JavaScript for falling rain animation with better effects
rain_animation = """
<style>
body {
    margin: 0;
    overflow: hidden;
    background: linear-gradient(to bottom, #2b5876, #4e4376);
    color: white;
    font-family: Arial, sans-serif;
}

#rain-canvas {
    position: fixed;
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
        opacity: Math.random() * 0.5 + 0.2,
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
    ctx.strokeStyle = "rgba(173, 216, 230, 0.8)";
    ctx.lineWidth = 1.5;
    raindrops.forEach((drop) => {
        ctx.globalAlpha = drop.opacity;
        ctx.beginPath();
        ctx.moveTo(drop.x, drop.y);
        ctx.lineTo(drop.x, drop.y + drop.length);
        ctx.stroke();
    });
    ctx.globalAlpha = 1;
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
    <h1 style="text-align: center; color: white;">🌦️ Rainfall Prediction Application</h1>
    <p style="text-align: center; color: lightgray;">
    Enter weather details to predict whether it will rain, and enjoy the dynamic rain effects if rainfall is predicted!
    </p>
    """,
    unsafe_allow_html=True,
)

# Input fields
st.sidebar.header("Enter Weather Details 🌤️")
inputs = {}
for feature in feature_names:
    inputs[feature] = st.sidebar.number_input(f"Enter {feature}", value=0.0)

# Prediction
input_df = pd.DataFrame([inputs.values()], columns=feature_names)
prediction = model.predict(input_df)[0]

# Display Result
if prediction == 1:
    st.markdown(
        "<h2 style='text-align: center; color: lightblue;'>🌧️ Rainfall is expected! Watch the rain animation!</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(rain_animation, unsafe_allow_html=True)
else:
    st.markdown(
        "<h2 style='text-align: center; color: lightgreen;'>☀️ No Rainfall is expected. Enjoy the sunshine!</h2>",
        unsafe_allow_html=True,
    )

# Footer
st.markdown(
    """
    <footer style="text-align: center; color: lightgray; margin-top: 20px;">
    Created with ❤️ by <b>Your Name</b> | Powered by Streamlit
    </footer>
    """,
    unsafe_allow_html=True,
)
