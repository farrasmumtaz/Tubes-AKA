import streamlit as st
import time
import sys

sys.setrecursionlimit(200000)

# -----------------------------
# Graph Generator (Cycle Eulerian)
# -----------------------------
def generate_cycle_graph(n):
    graph = {i: [] for i in range(n)}
    for i in range(n):
        u = i
        v = (i + 1) % n
        graph[u].append(v)
        graph[v].append(u)
    return graph

# -----------------------------
# Recursive Euler (Hierholzer)
# -----------------------------
def euler_recursive(u, graph, path):
    while graph[u]:
        v = graph[u].pop()
        graph[v].remove(u)
        euler_recursive(v, graph, path)
    path.append(u)

# -----------------------------
# Iterative Euler (Hierholzer)
# -----------------------------
def euler_iterative(start, graph):
    g = {u: list(adj) for u, adj in graph.items()}
    stack = [start]
    path = []

    while stack:
        u = stack[-1]
        if g[u]:
            v = g[u].pop()
            g[v].remove(u)
            stack.append(v)
        else:
            path.append(stack.pop())

    return path

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🔄 Perbandingan Algoritma Lintasan Euler")
st.markdown("""
Aplikasi ini membandingkan **algoritma Euler versi rekursif dan iteratif**
berdasarkan **waktu eksekusi**.
""")

n = st.slider(
    "Jumlah simpul (vertex)",
    min_value=100,
    max_value=50000,
    value=10000,
    step=1000
)

start_button = st.button("🚀 Jalankan Pengujian")

if start_button:
    st.info(f"Membuat graf Eulerian dengan {n} simpul...")
    graph = generate_cycle_graph(n)

    # -------- Iterative --------
    st.subheader("⚙️ Versi Iteratif")
    start = time.time()
    path_iter = euler_iterative(0, graph)
    t_iter = time.time() - start
    st.success(f"Waktu eksekusi iteratif: {t_iter:.6f} detik")

    # -------- Recursive --------
    st.subheader("🧠 Versi Rekursif")
    graph_copy = {u: list(adj) for u, adj in graph.items()}

    try:
        start = time.time()
        path_rec = []
        euler_recursive(0, graph_copy, path_rec)
        t_rec = time.time() - start
        st.success(f"Waktu eksekusi rekursif: {t_rec:.6f} detik")

        st.metric(
            "Iteratif lebih cepat (kali)",
            f"{t_rec / t_iter:.2f}×"
        )

    except RecursionError:
        st.error("❌ Rekursif gagal: RecursionError (stack overflow)")
        st.metric("Iteratif vs Rekursif", "Iteratif berhasil, Rekursif gagal")

    # -------- Summary --------
    st.subheader("📌 Kesimpulan")
    st.markdown("""
    - **Iteratif lebih stabil dan cepat**
    - **Rekursif tidak cocok untuk input besar**
    - Kompleksitas teoritis sama: **O(V + E)**
    - Perbedaan nyata muncul pada ukuran besar
    """)