import streamlit as st
import graphviz
import math
import pandas as pd
import itertools

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

# --- Sliders and UI Controls ---
staff_scale_input = st.slider("% of current staffing level", 32, 100, 100, format="%d%%")
staff_scale = (staff_scale_input - 29) * (100 / (100 - 29))

seniority_input = st.slider("Seniority afforded", 70, 100, 100, format="%d%%")  # default changed to 100%
seniority = (seniority_input - 76) * (100 / (100 - 76))

workers_per_mgr = st.slider("Learning technologists per manager", 5, 10, 10)
show_content_as_team = st.checkbox("Learning content as separate team", value=False)

chart_container = st.container()

# --- Team Counts ---
fss_num_staff = int(5 + (15 * staff_scale / 100))
system_num_staff = int(3 + (7 * staff_scale / 100))
content_num_staff = min(3, int(1 + (4 * staff_scale / 100)))
total_fss_workers = fss_num_staff + (0 if show_content_as_team else content_num_staff)
fss_num_managers = max(1, round(total_fss_workers / workers_per_mgr))

# --- Org Chart ---
dot = graphviz.Digraph(engine="circo")
dot.graph_attr.update(fontsize="6")
dot.node_attr.update(fontsize="6")
dot.edge_attr.update(fontsize="6")
dot.attr(ranksep="1.5", nodesep="1.0")
salary, spine = get_salary(6, seniority)
dot.node("Boss", f"""Director\nLevel 6-{spine:02}""", shape="hexagon")

# --- Staffing Table Generation ---
staff_rows = []

salary, spine = get_salary(6, seniority)
staff_rows.append({"Role": "Director", "Level": 6, "Spine Point": spine, "Salary": salary, "Team": "0_Director"})

# FSS Managers as individual nodes
fss_mgr_nodes = []
for i in range(fss_num_managers):
    mgr_id = f"FSS_Manager_{i+1}"
    salary, spine = get_salary(5, seniority)
    dot.node(mgr_id, f"""FSS manager\nLevel 5-{spine:02}""", shape="box", color="blue")
    dot.edge("Boss", mgr_id, color="blue", penwidth="2")
    salary, spine = get_salary(5, seniority)
    staff_rows.append({"Role": "FSS manager", "Level": 5, "Spine Point": spine, "Salary": salary, "Team": "1_FSS"})
    fss_mgr_nodes.append(mgr_id)

# Systems team
salary, spine = get_salary(5, seniority)
dot.node("Sys_Manager", f"""Systems manager\nLevel 5-{spine:02}""", shape="box", color="red")
dot.edge("Boss", "Sys_Manager", color="red", penwidth="2")
salary, spine = get_salary(5, seniority)
staff_rows.append({"Role": "Systems manager", "Level": 5, "Spine Point": spine, "Salary": salary, "Team": "2_Systems"})

# Content team manager (if shown separately)
if show_content_as_team:
    salary, spine = get_salary(5, seniority)
    dot.node("Content_Manager", f"""Content manager\nLevel 5-{spine:02}""", shape="box", color="green")
    dot.edge("Boss", "Content_Manager", color="green", penwidth="2")
    salary, spine = get_salary(5, seniority)
    staff_rows.append({"Role": "Content manager", "Level": 5, "Spine Point": spine, "Salary": salary, "Team": "3_Content"})

# --- Worker allocation helper ---
def calc_worker_allocation(seniority_pct):
    low_mix = {4: 0.25, 3: 0.5, 2: 0.25}
    high_mix = {4: 1.0, 3: 0.0, 2: 0.0}
    mix = {}
    for level in [4, 3, 2]:
        mix[level] = (seniority_pct / 100) * high_mix[level] + ((100 - seniority_pct) / 100) * low_mix[level]
    return [(level, proportion) for level, proportion in mix.items() if proportion > 0.01]

allocations = calc_worker_allocation(seniority)

# --- Create and assign workers ---
worker_counter = 0

def create_workers(team, count, parent_nodes):
    global worker_counter
    local_workers = []
    assigned = 0
    level_counts = []

    # Precompute exact worker counts per level using proportions
    for level, proportion in allocations:
        exact = count * proportion
        level_counts.append((level, exact))

    # Sort by descending exact so larger buckets are filled first
    level_counts.sort(key=lambda x: -x[1])

    for level, exact in level_counts:
        n = min(int(round(exact)), count - assigned)
        for _ in range(n):
            salary, spine = get_salary(level, seniority)
            role = f"{team}_Worker_{worker_counter}"
            worker_counter += 1
            if not show_content_as_team and team == "1_FSS" and role.startswith("1_FSS_Worker") and worker_counter > (fss_num_staff - 1):
                team_label = "Content"
            else:
                team_label = team.split('_')[1]
            role_label = f"{team_label} worker"
            color_map = {"FSS": "blue", "Systems": "red", "Content": "green"}
            color = color_map.get(team_label, "black")
            dot.node(role, f"""{role_label}
Level {level}-{spine:02}""", color=color)
            parent = next(parent_nodes)
            dot.edge(parent, role, color=color)
            staff_rows.append({"Role": role_label, "Level": level, "Spine Point": spine, "Salary": salary, "Team": team})
            local_workers.append(role)
            assigned += 1
            if assigned >= count:
                break
        if assigned >= count:
            break

    return local_workers

# Round-robin distribution to FSS managers
fss_mgr_cycle = itertools.cycle(fss_mgr_nodes)
create_workers("1_FSS", fss_num_staff, fss_mgr_cycle)

# Content workers: integrate with FSS or show separately
if show_content_as_team:
    create_workers("3_Content", content_num_staff, itertools.cycle(["Content_Manager"]))
else:
    create_workers("3_Content", content_num_staff, itertools.cycle([fss_mgr_nodes[0]]))

# Systems workers
create_workers("2_Systems", system_num_staff, itertools.cycle(["Sys_Manager"]))

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
    st.dataframe(df_table, hide_index=True)


