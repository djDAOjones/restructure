import streamlit as st
import graphviz

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("📇 Org Chart Builder")

# --- Initialize Graph ---
dot = graphviz.Digraph(engine="circo")  # Use circular layout
dot.attr(ranksep="1.5", nodesep="1.0")

# Boss node
dot.node("Boss", "Boss", shape="box")

# --- Sliders for each team ---
st.header("FSS Team (Formerly Learning Technologists)")
fss_num_managers = st.slider("Number of Co-Managers (FSS)", 1, 4, 2)
fss_num_staff = st.slider("Number of Staff (FSS)", 2, 20, 8)

st.header("System Team")
system_num_staff = st.slider("Number of System Workers", 1, 15, 5)

st.header("Learning Content Team")
content_num_staff = st.slider("Number of Learning Content Workers", 1, 15, 6)

# --- Build Org Chart ---
# FSS Leadership
fss_lead = "FSS_Lead"
fss_label = " / ".join(["FSS Manager"] * fss_num_managers)
dot.node(fss_lead, fss_label)
dot.edge("Boss", fss_lead)

# FSS Staff
for w in range(1, fss_num_staff + 1):
    worker = f"FSS_Worker{w}"
    dot.node(worker, f"FSS Staff {w}")
    dot.edge(fss_lead, worker)

# System Team
sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "System Manager")
dot.edge("Boss", sys_mgr)

for w in range(1, system_num_staff + 1):
    worker = f"Sys_Worker{w}"
    dot.node(worker, f"System Staff {w}")
    dot.edge(sys_mgr, worker)

# Learning Content Team
content_mgr = "LC_Manager"
dot.node(content_mgr, "Content Manager")
dot.edge("Boss", content_mgr)

for w in range(1, content_num_staff + 1):
    worker = f"LC_Worker{w}"
    dot.node(worker, f"Content Staff {w}")
    dot.edge(content_mgr, worker)

# --- Display chart at the top ---
st.subheader("📈 Org Chart Preview")
st.graphviz_chart(dot)
