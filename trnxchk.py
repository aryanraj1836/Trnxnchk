import streamlit as st
from colorama import Fore, Style, init
init()
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#defining all the functions for the tools
#function for graph 
def build_precedence_graph(conflicts):
    graph = nx.DiGraph()
    for op1, op2 in conflicts:
        graph.add_edge(f"T{op1[1]}", f"T{op2[1]}")
    return graph
#function for finding conflicts
def parse_operation(op):
    op = op.strip()
    if len(op) < 5:
        return None
    op_type = op[0]
    trnxn_id = op[1]
    data_item = op[3]
    return (op_type, trnxn_id, data_item)
#function for sorting conflicts into a list which gives out data for precedence graph
def find_conflicts(schedule):
    parsed = [parse_operation(op) for op in schedule]
    parsed = [p for p in parsed if p is not None]
    conflicts = []

    for i in range(len(parsed)):
        for j in range(i + 1, len(parsed)):
            op1 = parsed[i]
            op2 = parsed[j]

            same_data = op1[2] == op2[2]
            diff_txn = op1[1] != op2[1]
            one_write = op1[0] == 'W' or op2[0] == 'W'

            if same_data and diff_txn and one_write:
                conflicts.append((op1, op2))
    return conflicts
#functions for checking serializability
def check_serializability(graph):
    if nx.is_directed_acyclic_graph(graph):
       st.write( "\n Schedule is CONFLICT SERIALIZABLE")
    else:
        st.write( "\n Schedule is NOT CONFLICT SERIALIZABLE")
#User input
st.write("    TxnCheck — Transaction Serializability Checker    ")
st.write("Enter Read\Write operations one by one")
st.write("Type 'done' when finished\n")
schedule = st.text_area("Enter operations (one per line)", "")
schedule = [
    line.strip()
    for line in schedule.splitlines()
    if line.strip()]
conflicts = find_conflicts(schedule)
# Build blank slate graph
conflicts = find_conflicts(schedule)
st.write(f"\nConflicts found: {len(conflicts)}")
graph = build_precedence_graph(conflicts)
# Draw graph
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor('#1e1e2e')
ax.set_facecolor('#1e1e2e')
ax.axis('off')
pos = nx.spring_layout(graph)
nx.draw(graph, pos, ax=ax, with_labels=True,
        node_color='#89b4fa', edge_color='#f38ba8',
        font_color='white', font_size=14,
        font_weight='bold', node_size=3000,
        arrows=True, arrowsize=25)
ax.set_title("Precedence Graph", color='white', fontsize=16, fontweight='bold')
plt.tight_layout()
st.pyplot(fig)

# Final Verdict for Serializability
if st.button("Check Serializability"):
    check_serializability(graph)
