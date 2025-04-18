import streamlit as st
import graphviz

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("Restructure Chart")

# Salary data and cost multipliers
SALARY_COSTS = {
    "Level 6": 109480,  # Director
    "Level 5": 86498,   # Managers
    "Level 4": 55747    # Workers (senior)
}

# Seniority adjustment slider
seniority = st.slider("Global Staff Seniority (%)", 0, 100, 100)

# Estimate average worker cost based on seniority percentage
avg_worker_cost = round(SALARY_COSTS["Level 4"] * (seniority / 100) + SALARY_COSTS["Level 4"] * 0.7 * ((100 - seniority) / 100))

# Placeholder for cost calculation
costs = {
    "Director": SALARY_COSTS["Level 6"],
    "FSS Managers": 0,
    "FSS Workers": 0,
    "Systems Manager": SALARY_COSTS["Level 5"],
    "Systems Workers": 0,
    "Content Manager": SALARY_COSTS["Level 5"],
    "Content Workers": 0
}

# Reserve chart space early
chart_container = st.container()

# --- Sliders for each team ---
st.header("Faculty and School Support (FSS)")
fss_num_managers = st.slider("Number of Co-Managers (FSS)", 1, 4, 2)
fss_num_staff = st.slider("Number of Staff (FSS)", 5, 20, 8)

st.header("Learning Systems Team")
system_num_staff = st.slider("Number of Systems Workers", 3, 10, 5)

st.header("Learning Content Team")
content_num_staff = st.slider("Number of Learning Content Workers", 1, 5, 3)

# --- Build Org Chart ---
dot = graphviz.Digraph(engine="circo")
dot.attr(ranksep="1.5", nodesep="1.0")

dot.node("Boss", "Director", shape="box")

# FSS
fss_lead = "FSS_Lead"
fss_label = "
".join(["FSS Manager"] * fss_num_managers)
