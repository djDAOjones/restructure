import streamlit as st
import graphviz
import math

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("Restructure Chart")

# Predefined salary spine values (based on Excel data)
df_salaries = {
    13: 32100, 14: 32800, 15: 33600, 16: 34300, 17: 35100, 18: 36000, 19: 36800, 20: 37800,
    21: 38700, 22: 39600, 23: 41100, 24: 42300, 25: 43500, 26: 44400, 27: 45600, 28: 47000,
    29: 48300, 30: 49700, 31: 51100, 32: 52600, 33: 54100, 34: 55700, 35: 57400, 36: 59000,
    37: 60700, 38: 62600, 39: 64400, 40: 66400, 41: 68300, 42: 70400, 43: 72500, 44: 74600,
    45: 76900, 46: 79200, 47: 81500, 48: 84000, 49: 86500, 50: 89100, 51: 91700, 52: 94400,
    53: 97300, 54: 100200, 55: 103200, 56: 106300, 57: 109500
}

# Define spine ranges by level
SPINE_RANGES = {
    2: list(range(13, 23)),
    3: list(range(18, 28)),
    4: list(range(23, 33)),
    5: list(range(44, 54)),
    6: list(range(54, 64))
}

def get_salary(level, seniority_pct):
    if level not in SPINE_RANGES:
        return 0
    spine_range = SPINE_RANGES[level]
    index = int(round((seniority_pct / 100) * (len(spine_range) - 1)))
    spine_point = spine_range[index]
    return df_salaries.get(spine_point, 0), spine_point

# --- Global staffing level control ---
staff_scale = st.slider("Global Staffing Level (%)", 0, 100, 50, format="%d%%")
seniority = st.slider("Global Staff Seniority (% with full senior staff)", 0, 100, 100, format="%d%%")

# Reserve chart space early
chart_container = st.container()

# --- Sliders for each team ---
st.header("Faculty and School Support (FSS)")
fss_mgr_default = int(1 + (3 * staff_scale / 100))
fss_num_managers = st.slider("Number of Managers (FSS)", 1, 4, fss_mgr_default, key="fss_mgr_slider")
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

# System
sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "Systems Manager")
dot.edge("Boss", sys_mgr)

# Content
content_mgr = "LC_Manager"
dot.node(content_mgr, "Content Manager")
dot.edge("Boss", content_mgr)

# --- Detailed staff listing ---
st.markdown("### Full Staff Listing")
staff_rows = []

# Director
salary, spine = get_salary(6, seniority)
staff_rows.append({"Role": "Director", "Level": 6, "Spine Point": spine, "Salary": salary})

# Managers
for i in range(fss_num_managers):
    salary, spine = get_salary(5, seniority)
    staff_rows.append({"Role": "FSS Manager", "Level": 5, "Spine Point": spine, "Salary": salary})
salary, spine = get_salary(5, seniority)
staff_rows.append({"Role": "Systems Manager", "Level": 5, "Spine Point": spine, "Salary": salary})
staff_rows.append({"Role": "Content Manager", "Level": 5, "Spine Point": spine, "Salary": salary})

def calc_worker_allocation(seniority_pct):
    if seniority_pct == 0:
        return [(4, 0.25), (3, 0.5), (2, 0.25)]
    else:
        return [(4, 1.0)]

allocations = calc_worker_allocation(seniority)

# FSS workers
for level, proportion in allocations:
    count = math.ceil(fss_num_staff * proportion)
    for i in range(count):
        salary, spine = get_salary(level, seniority)
        label = f"FSS Staff {level}-{i+1}"
        dot.node(label, f"FSS Staff\nLevel {level}")
        dot.edge(fss_lead, label)
        staff_rows.append({"Role": "FSS Staff", "Level": level, "Spine Point": spine, "Salary": salary})

# Systems workers
for level, proportion in allocations:
    count = math.ceil(system_num_staff * proportion)
    for i in range(count):
        salary, spine = get_salary(level, seniority)
        label = f"Sys_Staff_{level}_{i+1}"
        dot.node(label, f"Systems Staff\nLevel {level}")
        dot.edge(sys_mgr, label)
        staff_rows.append({"Role": "Systems Staff", "Level": level, "Spine Point": spine, "Salary": salary})

# Content workers
for level, proportion in allocations:
    count = math.ceil(content_num_staff * proportion)
    for i in range(count):
        salary, spine = get_salary(level, seniority)
        label = f"Cont_Staff_{level}_{i+1}"
        dot.node(label, f"Content Staff\nLevel {level}")
        dot.edge(content_mgr, label)
        staff_rows.append({"Role": "Content Staff", "Level": level, "Spine Point": spine, "Salary": salary})

# --- Calculate costs ---
total_cost = sum(row["Salary"] for row in staff_rows)

# --- Render chart at the top ---
with chart_container:
    st.markdown(f"### 💷 Total Estimated Cost: £{total_cost:,.0f}")
    st.graphviz_chart(dot)

# Format salary
for row in staff_rows:
    row["Salary"] = f"£{row['Salary']:,.0f}"

# --- Display listing ---
with st.container():
    for row in staff_rows:
        st.markdown(f"**{row['Role']}**  ")
        st.markdown(f"Level {row['Level']} | Spine Point {row['Spine Point']} | Salary: {row['Salary']}")
        st.markdown("---")
