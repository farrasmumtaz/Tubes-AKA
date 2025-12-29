import streamlit as st
import time
import sys

# -----------------------------
# Konfigurasi
# -----------------------------
sys.setrecursionlimit(2000000)

# -----------------------------
# Graph Generator (Cycle Eulerian)
# -----------------------------
def generate_cycle_graph(n):
    graph = {i: [] for i in range(n)} # membuat graf kosong
    for i in range(n): 
        u = i #membuat simpul u
        v = (i + 1) % n #membuat simpul v
        graph[u].append(v) #menambahkan tetangga v ke u
        graph[v].append(u) #menambahkan tetangga u ke v
    return graph

# -----------------------------
# Recursive Euler (Hierholzer)
# -----------------------------
def euler_recursive(u, graph, path):
    while graph[u]: # selama masih ada tetangga
        v = graph[u].pop() # ambil tetangga v
        graph[v].remove(u) # hapus u dari tetangga v
        euler_recursive(v, graph, path) # rekursif ke v
    path.append(u) # tambahkan u ke lintasan

# -----------------------------
# Iterative Euler (Hierholzer)
# -----------------------------
def euler_iterative(start, graph):
    g = {u: list(adj) for u, adj in graph.items()} # salin graf
    stack = [start] # tumpukan untuk DFS
    path = [] # lintasan Euler

    while stack:
        u = stack[-1] # ambil simpul teratas
        if g[u]: # selama masih ada tetangga
            v = g[u].pop() # ambil tetangga v
            g[v].remove(u) # hapus u dari tetangga v
            stack.append(v) # dorong v ke tumpukan
        else:
            path.append(stack.pop()) # tambahkan u ke lintasan dan pop dari tumpukan

    return path

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Perbandingan Algoritma Euler", layout="centered")

st.title("🔄 Perbandingan Algoritma Lintasan Euler")
st.markdown("""
Aplikasi ini membandingkan **algoritma lintasan Euler versi iteratif dan rekursif**
berdasarkan **waktu eksekusi** menggunakan graf Eulerian berbentuk cycle.
""")

# Input ukuran graf
n = st.slider(
    "Jumlah simpul (vertex)",
    min_value=10,
    max_value=500000,
    value=10000,
    step=1000
)

start_button = st.button("🚀 Jalankan Pengujian")

# -----------------------------
# Eksekusi saat tombol ditekan
# -----------------------------
if start_button:
    st.info(f"Membuat graf Eulerian dengan {n} simpul...")
    graph = generate_cycle_graph(n)

    # -------- Iterative --------
    st.subheader("⚙️ Versi Iteratif")
    start_time = time.time()
    path_iter = euler_iterative(0, graph)
    t_iter = time.time() - start_time
    st.success(f"Waktu eksekusi iteratif: {t_iter:.6f} detik")

    # -------- Recursive --------
    st.subheader("🧠 Versi Rekursif")
    graph_copy = {u: list(adj) for u, adj in graph.items()}

    try:
        start_time = time.time()
        path_rec = []
        euler_recursive(0, graph_copy, path_rec)
        t_rec = time.time() - start_time
        st.success(f"Waktu eksekusi rekursif: {t_rec:.6f} detik")

        # -------- Perbandingan yang BENAR --------
        if t_iter < t_rec:
            st.metric(
                "Iteratif lebih cepat",
                f"{t_rec / t_iter:.2f}×"
            )
        else:
            st.metric(
                "Rekursif lebih cepat",
                f"{t_iter / t_rec:.2f}×"
            )

    except RecursionError:
        st.error("❌ Rekursif gagal: RecursionError (stack overflow)")
        st.metric("Perbandingan", "Iteratif berhasil, Rekursif gagal")

    # -------- Kesimpulan --------
    st.subheader("📌 Kesimpulan")
    st.markdown("""
- **Kedua algoritma memiliki kompleksitas teoritis yang sama: O(V + E)**  
- **Iteratif lebih stabil untuk graf berukuran besar**  
- **Rekursif dapat lebih cepat pada ukuran tertentu, tetapi berisiko stack overflow**  
- Perbedaan performa dipengaruhi oleh **overhead stack dan manajemen memori**
""")
