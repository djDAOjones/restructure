import streamlit as st
import graphviz
import math
import pandas as pd

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("Restructure Chart")

# --- Salary Spine Data (rounded to nearest £200 after 30% uplift) ---
df_salaries = {
    13: 32100, 14: 32800, 15: 33600, 16: 34400, 17: 35200, 18: 36000, 19: 36800, 20: 37800,
    21: 38600, 22: 39600, 23: 41200, 24: 42400, 25: 43600, 26: 44400, 27: 45600, 28: 47000,
    29: 48400, 30: 49800, 31: 51200, 32: 52600, 33: 54200, 34: 55800, 35: 57400, 36: 59000,
    37: 60800, 38: 62600, 39: 64400, 40: 66400, 41: 68400, 42: 70400, 43: 72600, 44: 74600,
    45: 77000, 46: 79400, 47: 81800, 48: 84200, 49: 86800, 50: 89400, 51: 92000, 52: 94600,
    53: 97400, 54: 100400, 55: 103400, 56: 106400, 57: 109600
}

SPINE_RANGES = {
    2: list(range(13, 23)),
    3: list(range(18, 28)),
    4: list(range(23, 33)),
    5: list(range(44, 54)),
    6: list(range(54, 58))
}

def get_salary(level, seniority_pct):
    if level not in SPINE_RANGES:
        return 0, 0
    spine_range = SPINE_RANGES[level]
    index = int(round((seniority_pct / 100) * (len(spine_range) - 1)))
    spine_point = spine_range[index]
    return df_salaries.get(spine_point, 0), spine_point

def interpolate_thickness_and_size(spine):
    low, mid, high = 13, 39, 52
    # Normalize between 0 and 1
    t = (spine - low) / (high - low)
    penwidth = 0.5 + (2.0 - 0.5) * t  # from 0.5 to 2.0
    size_factor = 0.8 + 0.4 * t       # from 0.8 to 1.2 (20% variation)
    return round(penwidth, 2), round(size_factor, 2)

# --- Sliders: UI shows real-world values, logic uses 0-100 internally ---
staff_scale_input = st.slider("% of current staffing level", 29, 100, 50, format="%d%%")
staff_scale = (staff_scale_input - 29) * (100 / (100 - 29))

seniority_input = st.slider("Seniority afforded", 76, 100, 100, format="%d%%")
seniority = (seniority_input - 76) * (100 / (100 - 76))

chart_container = st.container()

# --- Team Config ---
fss_mgr_default = int(1 + (3 * staff_scale / 100))
fss_num_managers = st.slider("FSS managers", 1, 4, fss_mgr_default, key="fss_mgr_slider")
fss_default = int(5 + (15 * staff_scale / 100))
fss_num_staff = st.slider("FSS workers", 5, 19, fss_default, key="fss_slider")

system_default = int(3 + (7 * staff_scale / 100))
system_num_staff = st.slider("Systems team workers", 3, 10, system_default, key="system_slider")

content_default = min(3, int(1 + (4 * staff_scale / 100)))
content_num_staff = st.slider("Learning content workers", 1, 3, content_default, key="content_slider")

# --- Org Chart ---
dot = graphviz.Digraph(engine="circo")
dot.attr(ranksep="1.5", nodesep="1.0")
dot.node("Boss", "Director", shape="box")

fss_lead = "FSS_Lead"
fss_label = " / ".join(["FSS Manager"] * fss_num_managers)
dot.node(fss_lead, fss_label)
dot.edge("Boss", fss_lead)

sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "Systems manager")
dot.edge("Boss", sys_mgr)

content_mgr = "LC_Manager"
dot.node(content_mgr, "Content manager")
dot.edge("Boss", content_mgr)

# --- Staffing Table Generation ---
staff_rows = []

salary, spine = get_salary(6, seniority)
staff_rows.append({"Role": "Director", "Level": 6, "Spine Point": spine, "Salary": salary, "Team": "0_Director"})

for i in range(fss_num_managers):
    salary, spine = get_salary(5, seniority)
    staff_rows.append({"Role": "FSS Manager", "Level": 5, "Spine Point": spine, "Salary": salary, "Team": "1_FSS"})

for role in ["Systems Manager", "Content Manager"]:
    salary, spine = get_salary(5, seniority)
    team = "2_Systems" if "Systems" in role else "3_Content"
    role_name = "Systems manager" if team == "2_Systems" else "Content manager"
    staff_rows.append({"Role": role_name, "Level": 5, "Spine Point": spine, "Salary": salary, "Team": team})

def calc_worker_allocation(seniority_pct):
    low_mix = {4: 0.25, 3: 0.5, 2: 0.25}
    high_mix = {4: 1.0, 3: 0.0, 2: 0.0}
    mix = {}
    for level in [4, 3, 2]:
        mix[level] = (seniority_pct / 100) * high_mix[level] + ((100 - seniority_pct) / 100) * low_mix[level]
    return [(level, proportion) for level, proportion in mix.items() if proportion > 0.01]

allocations = calc_worker_allocation(seniority)

for level, proportion in allocations:
    for team, parent, count in [
        ("1_FSS", fss_lead, fss_num_staff),
        ("2_Systems", sys_mgr, system_num_staff),
        ("3_Content", content_mgr, content_num_staff)
    ]:
        for i in range(math.ceil(count * proportion)):
            salary, spine = get_salary(level, seniority)
            label = f"{team}_Staff_{level}_{i+1}"
            team_name = team.split('_')[1]
            if team_name == "FSS":
                role_label = "FSS worker"
            elif team_name == "Systems":
                role_label = "Systems worker"
            else:
                role_label = "Content worker"
            penwidth, size = interpolate_thickness_and_size(spine)
            dot.node(label, f"{role_label}\nLevel {level}\nSpine {spine}", penwidth=str(penwidth), width=str(size), height=str(size))
            dot.edge(parent, label)
            staff_rows.append({"Role": role_label, "Level": level, "Spine Point": spine, "Salary": salary, "Team": team})

# --- Chart Output ---
total_cost = sum(row["Salary"] for row in staff_rows)
with chart_container:
    st.markdown(f"<p style='font-size:0.9em; font-weight:600;'>Total Estimated Cost: £{total_cost:,.0f}</p>", unsafe_allow_html=True)
    st.graphviz_chart(dot)

# --- Staff Listing Table ---
for row in staff_rows:
    row["Salary"] = f"£{row['Salary']:,.0f}"

if staff_rows:
    st.markdown("<p style='font-size:0.9em; font-weight:600;'>Full Staff Listing</p>", unsafe_allow_html=True)
    df_table = pd.DataFrame([{
        "role name": row["Role"],
        "team": row["Team"],
        "level": row["Level"],
        "spline": row["Spine Point"],
        "cost": row["Salary"]
    } for row in staff_rows])

    df_table.sort_values(by=["team", "role name", "level", "spline"], inplace=True)
    df_table.drop(columns=["team"], inplace=True)
    st.table(df_table)
