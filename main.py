import streamlit as st

# Konfigurasi halaman utama
st.set_page_config(page_title="Dashboard Cashloan - PT. Satutstop Finansial Solusi", page_icon="📊", layout="wide")

# Header dengan desain lebih menarik
st.markdown(
    """
    <div style='background-color: #2E4C6D; padding: 15px; border-radius: 10px; text-align: center;'>
        <h1 style='color: white;'>📊 Sanders Data Support Dashboard</h1>
        <p style='color: lightgray; font-size:18px;'></div>
    """,
    unsafe_allow_html=True
)

# Sidebar untuk navigasi otomatis
st.sidebar.success("Gunakan sidebar untuk navigasi antara halaman!")

st.write("Pilih salah satu halaman dari sidebar untuk melihat laporan Payday atau Personal Loan.")