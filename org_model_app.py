import streamlit as st
import graphviz

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("Restructure Chart")

# Predefined salary spine values (based on Excel data)
df_salaries = {
    13: 32000,
    14: 33000,
    15: 33500,
    16: 34000,
    17: 35000,
    18: 36000,
    19: 37000,
    20: 38000,
    21: 39000,
    22: 40000,
    23: 41000,
    24: 42000,
    25: 44000,
    26: 45000,
    27: 46000,
    28: 47000,
    29: 48000,
    30: 50000,
    31: 51000,
    32: 52000,
    33: 54000,
    34: 55000,
    35: 57000,
    36: 58000,
    37: 60000,
    38: 62000,
    39: 63000,
    40: 65000,
    41: 67000,
    42: 69000,
    43: 71000,
    44: 73000,
    45: 75000,
    46: 77000,
    47: 80000,
    48: 82000,
    49: 84000,
    50: 86000,
    51: 89000,
    52: 91000,
    53: 94000,
    54: 97000,
    55: 100000
}

# Salary data and cost multipliers
SALARY_COSTS = {
    "Level 6": 109480,  # Director
    "Level 5": 86498,   # Managers
    "Level 4": 55747    # Workers (senior)
}



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

# --- Global staffing level control ---
staff_scale = st.slider("Global Staffing Level (%)", 0, 100, 50, format="%d%%")
seniority = st.slider("Global Staff Seniority (% with full senior staff)", 0, 100, 100, format="%d%%")

# Reserve chart space early
chart_container = st.container()

# Estimate average worker cost based on seniority percentage
avg_worker_cost = round(SALARY_COSTS["Level 4"] * (seniority / 100) + SALARY_COSTS["Level 4"] * 0.7 * ((100 - seniority) / 100))

# --- Sliders for each team ---
st.header("Faculty and School Support (FSS)")
fss_num_managers = st.slider("Number of Managers (FSS)", 1, 4, 2)
fss_default = int(5 + (15 * staff_scale / 100))
fss_num_staff = st.slider("Number of Staff (FSS)", 5, 20, fss_default, key="fss_slider")

st.header("Learning Systems Team")
system_default = int(3 + (7 * staff_scale / 100))
system_num_staff = st.slider("Number of Systems Workers", 3, 10, system_default, key="system_slider")

st.header("Learning Content Team")
content_default = int(1 + (4 * staff_scale / 100))
content_num_staff = st.slider("Number of Learning Content Workers", 1, 5, content_default, key="content_slider")

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
costs["FSS Workers"] = fss_num_staff * avg_worker_cost
costs["System Workers"] = system_num_staff * avg_worker_cost
costs["Content Workers"] = content_num_staff * avg_worker_cost
total_cost = sum(costs.values())

# --- Render chart at the top ---
with chart_container:
    st.markdown(f"### 💷 Total Estimated Cost: £{total_cost:,.0f}")
    st.graphviz_chart(dot)

# --- Team cost breakdown ---
st.markdown("### Cost Breakdown by Team")
st.table({
    "Team": list(costs.keys()),
    "Estimated Cost (£)": [f"£{v:,.0f}" for v in costs.values()]
})

# --- Detailed staff listing ---
st.markdown("### Full Staff Listing")
staff_rows = []

# Director
staff_rows.append({"Role": "Director", "Level": 6, "Spine Point": 55, "Salary": 84116, "Org Cost": SALARY_COSTS["Level 6"]})

# Managers
for i in range(fss_num_managers):
    staff_rows.append({"Role": "FSS Manager", "Level": 5, "Spine Point": 44, "Salary": 66460, "Org Cost": SALARY_COSTS["Level 5"]})
staff_rows.append({"Role": "Systems Manager", "Level": 5, "Spine Point": 44, "Salary": 66460, "Org Cost": SALARY_COSTS["Level 5"]})
staff_rows.append({"Role": "Content Manager", "Level": 5, "Spine Point": 44, "Salary": 66460, "Org Cost": SALARY_COSTS["Level 5"]})

# Workers at lower seniority
import math

def calc_worker_allocation(seniority_pct):
    if seniority_pct == 0:
        return [(4, 0.25), (3, 0.5), (2, 0.25)]
    else:
        return [(4, 1.0)]

def calc_worker_salary(level):
    if level == 4:
        return df_salaries[23]
    elif level == 3:
        return df_salaries[18]
    elif level == 2:
        return round(SALARY_COSTS["Level 4"] * 0.4)

allocations = calc_worker_allocation(seniority)

# FSS workers
for level, proportion in allocations:
    count = math.ceil(fss_num_staff * proportion)
    for i in range(count):
        salary = calc_worker_salary(level)
        label = f"FSS Staff {level}-{i+1}"
        dot.node(label, f"FSS Staff\nLevel {level}")
        dot.edge(fss_lead, label)
        staff_rows.append({"Role": "FSS Staff", "Level": level, "Spine Point": 20, "Salary": salary, "Org Cost": salary})

# Systems workers
for level, proportion in allocations:
    count = math.ceil(system_num_staff * proportion)
    for i in range(count):
        salary = calc_worker_salary(level)
        label = f"Sys_Staff_{level}_{i+1}"
        dot.node(label, f"Systems Staff\nLevel {level}")
        dot.edge(sys_mgr, label)
        staff_rows.append({"Role": "Systems Staff", "Level": level, "Spine Point": 20, "Salary": salary, "Org Cost": salary})

# Content workers
for level, proportion in allocations:
    count = math.ceil(content_num_staff * proportion)
    for i in range(count):
        salary = calc_worker_salary(level)
        label = f"Cont_Staff_{level}_{i+1}"
        dot.node(label, f"Content Staff\nLevel {level}")
        dot.edge(content_mgr, label)
        staff_rows.append({"Role": "Content Staff", "Level": level, "Spine Point": 20, "Salary": salary, "Org Cost": salary})

for row in staff_rows:
    row["Salary"] = f"£{row['Salary']:,.0f}"
    row["Org Cost"] = f"£{row['Org Cost']:,.0f}"

st.dataframe(staff_rows)
