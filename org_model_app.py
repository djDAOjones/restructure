import streamlit as st
import math

st.set_page_config(page_title="Org Restructure Model", layout="centered")

st.title("🔧 Org Restructure Model")
st.write("Model potential org structures by adjusting managers, worker ratios, or total headcount.")

# --- Mode toggle ---
mode = st.radio("Select mode:", ["Input managers + ratio", "Input target workers + ratio"])

# --- Common input ---
workers_per_manager = st.slider("Workers per Manager", min_value=2, max_value=10, value=5)

# --- Fixed boss ---
num_bosses = 1

# --- Mode 1: Input number of managers ---
if mode == "Input managers + ratio":
    num_managers = st.slider("Number of Managers (Level 5)", min_value=1, max_value=4, value=2)
    num_workers = num_managers * workers_per_manager

# --- Mode 2: Input target workers, calculate needed managers ---
else:
    num_workers = st.slider("Target Total Workers (Level 2–4)", min_value=10, max_value=35, value=20)
    num_managers = math.ceil(num_workers / workers_per_manager)

# --- Total count ---
total_employees = num_bosses + num_managers + num_workers

# --- Worker level breakdown ---
st.subheader("🔢 Structure Breakdown")
st.write(f"👑 Bosses (Level 6): {num_bosses}")
st.write(f"🧑‍💼 Managers (Level 5): {num_managers}")
st.write(f"🛠️ Workers (Levels 2–4): {num_workers}")
st.write(f"📊 Total Employees: **{total_employees}**")

# --- Breakdown of worker levels ---
st.subheader("📉 Worker Level Breakdown (Estimated Split)")
level_4 = int(num_workers * 0.4)
level_3 = int(num_workers * 0.35)
level_2 = num_workers - level_4 - level_3

col1, col2, col3 = st.columns(3)
col1.metric("Level 4", level_4)
col2.metric("Level 3", level_3)
col3.metric("Level 2", level_2)

# --- Optional: Org Summary Table ---
st.subheader("📋 Summary Table")
st.table({
    "Level": ["6 (Boss)", "5 (Manager)", "4", "3", "2"],
    "Count": [num_bosses, num_managers, level_4, level_3, level_2]
})

# Optional stretch goal: Graphviz org chart rendering could go here
