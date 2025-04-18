import streamlit as st
import math

# --- PAGE SETUP ---
st.set_page_config(page_title="Org Structure Model", layout="centered")
st.title("🏗️ Org Restructure Model")
st.write("Model your org structure by adjusting the number of workers or managers.")

# --- INPUT MODE SELECTION ---
input_mode = st.selectbox("What do you want to input?", ["Number of Managers", "Number of Workers"])
workers_per_manager = st.slider("Workers per Manager", min_value=2, max_value=10, value=5)

# --- DYNAMIC LOGIC BASED ON INPUT MODE ---
if input_mode == "Number of Managers":
    num_managers = st.slider("Number of Managers (Level 5)", min_value=1, max_value=4, value=2)
    num_workers = num_managers * workers_per_manager
else:
    num_workers = st.slider("Target Number of Workers (Level 2–4)", min_value=10, max_value=35, value=20)
    num_managers = math.ceil(num_workers / workers_per_manager)

# --- STATIC VALUES ---
num_bosses = 1
total_employees = num_bosses + num_managers + num_workers

# --- HEADCOUNT LIMIT ---
max_headcount = st.number_input("Max Total Employees Allowed", value=40)

if total_employees > max_headcount:
    st.warning(f"⚠️ This structure exceeds your headcount limit of {max_headcount}!")
else:
    st.success(f"✅ Headcount is within the allowed limit.")

# --- STRUCTURE OVERVIEW ---
st.subheader("📊 Structure Summary")
st.write(f"Bosses (Level 6): {num_bosses}")
st.write(f"Managers (Level 5): {num_managers}")
st.write(f"Workers (Level 2–4): {num_workers}")
st.write(f"Total Employees: **{total_employees}**")

# --- WORKER LEVEL BREAKDOWN ---
st.subheader("📉 Worker Level Breakdown (Est. Split)")
level_4 = int(num_workers * 0.4)
level_3 = int(num_workers * 0.35)
level_2 = num_workers - level_4 - level_3

col1, col2, col3 = st.columns(3)
col1.metric("Level 4", level_4)
col2.metric("Level 3", level_3)
col3.metric("Level 2", level_2)

# --- ORG CHART ---
st.subheader("📈 Org Chart Preview")

# Add spacer to simulate height
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# Build DOT string manually
dot_string = "digraph G {\n"
dot_string += 'Boss [label="Boss", shape="box"];\n'

# Managers
for m in range(num_managers):
    manager_id = f"Manager{m+1}"
    dot_string += f'{manager_id} [label="{manager_id}"];\n'
    dot_string += f'Boss -> {manager_id};\n'

# Workers
worker_id = 1
for m in range(num_managers):
    manager_id = f"Manager{m+1}"
    for _ in range(workers_per_manager):
        if worker_id > num_workers:
            break
        worker_label = f"Worker{worker_id}"
        dot_string += f'{worker_label} [label="{worker_label}"];\n'
        dot_string += f'{manager_id} -> {worker_label};\n'
        worker_id += 1

dot_string += "}"

# Render org chart
st.graphviz_chart(dot_string)

# Add another spacer after chart
st.markdown("<div style='height:300px'></div>", unsafe_allow_html=True)

# Alt-text for accessibility
st.markdown(
    f"**Alt-text:** 1 Boss → {num_managers} Managers → {num_workers} Workers " +
    f"({workers_per_manager} per manager)"
)
