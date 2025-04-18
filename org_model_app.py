import streamlit as st
import graphviz

st.set_page_config(page_title="Org Chart", layout="centered")
st.title("🏗️ Org Chart Builder")

# --- Sliders for each team ---
st.header("Learning Technologists Team")
lt_num_managers = st.slider("Number of Co-Managers", 1, 4, 2)
lt_num_staff = st.slider("Number of Staff (Learning Technologists)", 2, 20, 8)

st.header("System Team")
system_num_staff = st.slider("Number of System Workers", 1, 15, 5)

st.header("Learning Content Team")
content_num_staff = st.slider("Number of Learning Content Workers", 1, 15, 6)

# --- Build Org Chart ---
dot = graphviz.Digraph(engine="dot")
dot.attr(ranksep="1.5", nodesep="1.0")

# Boss node
dot.node("Boss", "👑 Boss", shape="box")

# --- Learning Technologists Team ---
lt_lead = "LT_Lead"
dot.node(lt_lead, "🧑‍💼 LT Manager")
dot.edge("Boss", lt_lead)

for i in range(lt_num_managers - 1):
    co_mgr = f"LT_Co{i+1}"
    dot.node(co_mgr, f"🤝 LT Co-Mgr {i+1}")
    dot.edge("Boss", co_mgr)

for w in range(1, lt_num_staff + 1):
    worker = f"LT_Worker{w}"
    dot.node(worker, f"🛠️ LT Staff {w}")
    dot.edge(lt_lead, worker)
    for i in range(lt_num_managers - 1):
        co_mgr = f"LT_Co{i+1}"
        dot.edge(co_mgr, worker)

# --- System Team ---
sys_mgr = "Sys_Manager"
dot.node(sys_mgr, "🧑‍💼 System Manager")
dot.edge("Boss", sys_mgr)

for w in range(1, system_num_staff + 1):
    worker = f"Sys_Worker{w}"
    dot.node(worker, f"🛠️ Sys Staff {w}")
    dot.edge(sys_mgr, worker)

# --- Learning Content Team ---
content_mgr = "LC_Manager"
dot.node(content_mgr, "🧑‍💼 Content Manager")
dot.edge("Boss", content_mgr)

for w in range(1, content_num_staff + 1):
    worker = f"LC_Worker{w}"
    dot.node(worker, f"🛠️ Content Staff {w}")
    dot.edge(content_mgr, worker)

# --- Render Org Chart ---
st.subheader("📈 Org Chart")
st.graphviz_chart(dot)
