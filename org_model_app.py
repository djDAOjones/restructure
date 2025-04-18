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
    "System Manager": SALARY_COSTS["Level 5"],
    "System Workers": 0,
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
system_num_staff = st.slider("Number of System Workers", 3, 10, 5)

st.header("Learning Content Team")
content_num_staff = st.slider("Number of Learning Content Workers", 1, 5, 3)

# --- Build Org Chart ---
dot = graphviz.Digraph(engine="circo")
dot.attr(ranksep="1.5", nodesep="1.0")

dot.node("Boss", "Director", shape="box")

# FSS
fss_lead = "FSS_Lead"
fss_label = " / ".join(["FSS Manager"] * fss_num_managers)
dot.node(fss_lead, fss_label)
dot.edge("Boss", fss_lead)
for w in range(1, fss_num_staff + 1):
    worker = f"FSS_Worker{w}"
    dot.node(worker, f"FSS Staff {w}")
    dot.edge(fss_lead, worker)

# System
sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "Systems Manager")
dot.edge("Boss", sys_mgr)
for w in range(1, system_num_staff + 1):
    worker = f"Sys_Worker{w}"
    dot.node(worker, f"System Staff {w}")
    dot.edge(sys_mgr, worker)

# Content
content_mgr = "LC_Manager"
dot.node(content_mgr, "Content Manager")
dot.edge("Boss", content_mgr)
for w in range(1, content_num_staff + 1):
    worker = f"LC_Worker{w}"
    dot.node(worker, f"Content Staff {w}")
    dot.edge(content_mgr, worker)

# --- Calculate costs ---
costs["FSS Managers"] = fss_num_managers * SALARY_COSTS["Level 5"]
costs["FSS Workers"] = fss_num_staff * avg_worker_cost
costs["System Workers"] = system_num_staff * avg_worker_cost
costs["Content Workers"] = content_num_staff * avg_worker_cost

total_cost = sum(costs.values())

# --- Display total cost at top ---
st.markdown(f"### 💷 Total Estimated Cost: £{total_cost:,.0f}")

# --- Render chart at the top ---
with chart_container:
    st.graphviz_chart(dot)

# --- Team cost breakdown ---
st.markdown("### Cost Breakdown by Team")
st.table({
    "Team": list(costs.keys()),
    "Estimated Cost (£)": [f"£{v:,.0f}" for v in costs.values()]
})