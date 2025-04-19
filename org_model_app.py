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

COLOR_LOW = (0, 128, 0)  # Green
COLOR_HIGH = (255, 51, 51)  # Red

def interpolate_color(level, spine):
    spine_range = SPINE_RANGES.get(level)
    if not spine_range:
        return "#999999"
    t = (spine - spine_range[0]) / (spine_range[-1] - spine_range[0])
    r = int(COLOR_LOW[0] + (COLOR_HIGH[0] - COLOR_LOW[0]) * t)
    g = int(COLOR_LOW[1] + (COLOR_HIGH[1] - COLOR_LOW[1]) * t)
    b = int(COLOR_LOW[2] + (COLOR_HIGH[2] - COLOR_LOW[2]) * t)
    return f"#{r:02X}{g:02X}{b:02X}"

def get_salary(level, seniority_pct):
    if level not in SPINE_RANGES:
        return 0, 0
    spine_range = SPINE_RANGES[level]
    index = int(round((seniority_pct / 100) * (len(spine_range) - 1)))
    spine_point = spine_range[index]
    return df_salaries.get(spine_point, 0), spine_point

# --- Sliders ---
staff_scale = st.slider("Number of staff", 29, 100, 50, format="%d%%")
seniority = st.slider("Seniority afforded", 76, 100, 100, format="%d%%")
chart_container = st.container()

# --- Team Config ---
st.markdown("<p style='font-size:0.9em; font-weight:600;'>Faculty and School Support (FSS)</p>", unsafe_allow_html=True)
fss_mgr_default = int(1 + (3 * staff_scale / 100))
fss_num_managers = st.slider("Number of Managers (FSS)", 1, 4, fss_mgr_default, key="fss_mgr_slider")
fss_default = int(5 + (15 * staff_scale / 100))
fss_num_staff = st.slider("Number of Staff (FSS)", 5, 20, fss_default, key="fss_slider")

st.markdown("<p style='font-size:0.9em; font-weight:600;'>Learning Systems Team</p>", unsafe_allow_html=True)
system_default = int(3 + (7 * staff_scale / 100))
system_num_staff = st.slider("Number of Systems Workers", 3, 10, system_default, key="system_slider")

st.markdown("<p style='font-size:0.9em; font-weight:600;'>Learning Content Team</p>", unsafe_allow_html=True)
content_default = int(1 + (4 * staff_scale / 100))
content_num_staff = st.slider("Number of Learning Content Workers", 1, 5, content_default, key="content_slider")

# --- Org Chart ---
dot = graphviz.Digraph(engine="circo")
dot.attr(ranksep="1.5", nodesep="1.0")
dot.node("Boss", "Director", shape="box", color=interpolate_color(6, SPINE_RANGES[6][-1]))

fss_lead = "FSS_Lead"
fss_label = " / ".join(["FSS Manager"] * fss_num_managers)
dot.node(fss_lead, fss_label, color=interpolate_color(5, SPINE_RANGES[5][-1]))
dot.edge("Boss", fss_lead)

sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "Systems Manager", color=interpolate_color(5, SPINE_RANGES[5][-1]))
dot.edge("Boss", sys_mgr)

content_mg