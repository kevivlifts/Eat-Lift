import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. Setup Gemini (Get your free key at aistudio.google.com)
genai.configure(api_key="# Secure way to load the key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Monte Linzor Tracker", layout="centered")

# Initialize Session State for Water if it doesn't exist
if 'water_ml' not in st.session_state:
    st.session_state.water_ml = 0

# --- SIDEBAR PROGRESS ---
with st.sidebar:
    st.title("🚢 Daily Stats")
    st.metric("Water Intake", f"{st.session_state.water_ml} ml")
    st.progress(min(st.session_state.water_ml / 4000, 1.0)) # Goal: 4L for high heat
    st.write("Goal: 4000ml (Engine Room Std)")

st.title("⚓ Engine Room Fitness AI")

tab1, tab2, tab3, tab4 = st.tabs(["🏋️ Lifts", "🍎 Food AI", "💧 Water", "📈 Progress"])

# --- TAB 1: WORKOUTS ---
with tab1:
    st.subheader("Log Your Sets")
    exercise = st.selectbox("Exercise", ["Bench Press", "Dumbell Flys", "Bulgarian Split Squats", "Leg Extension", "RDL", "Squats", "Deadlift", "Overhead Press", "Lateral Raise", "Rows", "Wide Lat Pulldown", "Close Grip Pulldown", "Hyperextension", "Chest Supported Rows" "Incline Curls", "Preacher Curls", "Hammer Curls", "Triceps Pushdowns", "Overhead Triceps Extension", "Cable Crunches"])
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", value=60, step=1)
    with col2:
        reps = st.number_input("Reps", value=10, step=1)
    
    if st.button("Log Lift", use_container_width=True):
        st.success(f"Logged: {exercise} - {weight}kg x {reps}")

# --- TAB 2: FOOD AI ---
with tab2:
    st.subheader("AI Calorie Counter")
    img_file = st.file_uploader("Snap a photo of your plate", type=['jpg', 'png', 'jpeg'])
    description = st.text_input("Or describe your meal (e.g., '2 chapatis and chicken curry')")
    
    if st.button("Analyze with Gemini", use_container_width=True):
        with st.spinner("Calculating..."):
            prompt = "Estimate calories and protein for this meal. Be very brief."
            response = model.generate_content([prompt, img_file] if img_file else prompt)
            st.info(response.text)

# --- TAB 3: WATER TRACKER ---
with tab3:
    st.subheader("Hydration Tracker")
    st.write("Working in 38°C+ requires constant fluid replacement.")
    
    c1, c2, c3 = st.columns(3)
    if c1.button("+250ml"):
        st.session_state.water_ml += 250
    if c2.button("+500ml"):
        st.session_state.water_ml += 500
    if c3.button("Reset"):
        st.session_state.water_ml = 0
    
    st.info(f"Total so far: {st.session_state.water_ml} ml")

# --- TAB 4: PROGRESS ---
with tab4:
    st.subheader("Weight Goal: 80kg")
    current_weight = st.number_input("Log Current Weight (kg)", value=104.0)
    st.write(f"Target: 80kg | To go: {round(current_weight - 80, 1)} kg")
