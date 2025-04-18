import streamlit as st
import graphviz

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("🏗️ Org Chart Builder")

# --- Sliders for each team ---
st.header("FSS Team (Formerly Learning Technologists)")
fss_num_managers = st.slider("Number of Co-Managers (FSS)", 1, 4, 2)
fss_num_staff = st.slider("Number of Staff (FSS)", 2, 20, 8)

st.header("System Team")
system_num_staff = st.slider("Number of System Workers", 1, 15, 5)

st.header("Learning Content Team")
content_num_staff = st.slider("Number of Learning Content Workers", 1, 15, 6)

# --- Build Org Chart ---
dot = graphviz.Digraph(engine="circo")  # Use circular layout
dot.attr(ranksep="1.5", nodesep="1.0")

# Boss node
dot.node("Boss", "Boss", shape="box")

# --- FSS Leadership Cluster ---
fss_lead = "FSS_Lead"

with dot.subgraph(name="cluster_fss_leads") as c:
    c.attr(label="FSS Leadership")
    c.attr(style="dashed")
    c.node(fss_lead, "FSS Manager")

    for i in range(fss_num_managers - 1):
        co_mgr = f"FSS_Co{i+1}"
        c.node(co_mgr, f"FSS Co-Mgr {i+1}")

# Edges from boss to FSS leadership
dot.edge("Boss", fss_lead)
for i in range(fss_num_managers - 1):
    co_mgr = f"FSS_Co{i+1}"
    dot.edge("Boss", co_mgr)

# Workers report only to the main manager
for w in range(1, fss_num_staff + 1):
    worker = f"FSS_Worker{w}"
    dot.node(worker, f"FSS Staff {w}")
    dot.edge(fss_lead, worker)

# --- System Team ---
sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "System Manager")
dot.edge("Boss", sys_mgr)

for w in range(1, system_num_staff + 1):
    worker = f"Sys_Worker{w}"
    dot.node(worker, f"System Staff {w}")
    dot.edge(sys_mgr, worker)

# --- Learning Content Team ---
content_mgr = "LC_Manager"
dot.node(content_mgr, "Content Manager")
dot.edge("Boss", content_mgr)

for w in range(1, content_num_staff + 1):
    worker = f"LC_Worker{w}"
    dot.node(worker, f"Content Staff {w}")
    dot.edge(content_mgr, worker)

# --- Display chart ---
st.subheader("📈 Org Chart")
st.graphviz_chart(dot)
