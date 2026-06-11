TrxnCheck — Transaction Serializability Checker
->A Python tool that checks whether a DBMS transaction schedule is **conflict serializable** using precedence graphs and cycle detection. Built with Streamlit for an interactive UI.

What it does?
-> Given a sequence of read/write operations from multiple transactions, TxnCheck:
- Identifies all conflicting operations (same data item, different transactions, at least one write)
- Builds a precedence graph from these conflicts
- Detects cycles to determine if the schedule is conflict serializable
- Visualizes the precedence graph

How it works?
1. Enter operations one per line in the format R1(A) (Read by T1 on item A) or W2(B) (Write by T2 on item B)
2. The tool parses each operation and finds conflicting pairs
3. A directed precedence graph is built from these conflicts
4. If the graph has a cycle -> NOT conflict serializable
5. If the graph is acyclic -> Conflict serializable
