import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ✅ Atur limit maksimum elemen yang bisa dirender dengan Pandas Styler
pd.set_option("styler.render.max_elements", 600000)  # Sesuaikan jika perlu

# **Membaca data**
try:
    df_lender_investment = pd.read_csv("data/lender_investment.csv")
except FileNotFoundError:
    st.error("⚠️ File tidak ditemukan! Pastikan file CSV berada di folder yang benar.")
    st.stop()

# **Membersihkan nama kolom dari spasi**
df_lender_investment.columns = df_lender_investment.columns.str.strip()

# **Debug: tampilkan kolom yang tersedia**
st.write("📋 Kolom dalam data:", df_lender_investment.columns.tolist())

# **Validasi apakah kolom 'investment_date' ada dan ubah ke datetime**
if "investment_date" in df_lender_investment.columns:
    df_lender_investment["investment_date"] = pd.to_datetime(
        df_lender_investment["investment_date"], errors="coerce"
    )
else:
    st.error("⚠️ Kolom 'investment_date' tidak ditemukan dalam CSV!")
    st.stop()

# **Navigasi Dashboard**
page = st.sidebar.radio("📌 Navigasi", ["Data Terfilter", "Grafik Investasi Lender"])

# **Dropdown untuk memilih Lender Name**
if "id_lender" in df_lender_investment.columns:
    lender_names = ["Semua Lender"] + list(df_lender_investment["id_lender"].dropna().unique())
    selected_lender = st.sidebar.selectbox("📌 Pilih Lender", lender_names)
else:
    st.error("⚠️ Kolom 'id_lender' tidak ditemukan dalam CSV!")
    st.stop()

# **Dropdown untuk memilih Date Investment**
date_options = ["Semua Tanggal"] + list(
    df_lender_investment["investment_date"]
    .dropna()
    .dt.strftime("%Y-%m-%d")
    .unique()
)
selected_date = st.sidebar.selectbox("📅 Pilih Tanggal Investasi", date_options)

# **Filter Data**
filtered_df = df_lender_investment[
    ((df_lender_investment["id_lender"] == selected_lender) | (selected_lender == "Semua Lender")) &
    ((df_lender_investment["investment_date"].dt.strftime("%Y-%m-%d") == selected_date) | (selected_date == "Semua Tanggal"))
]

# ============================
# 📄 Halaman Data Terfilter
# ============================
if page == "Data Terfilter":
    st.header("📊 Data Investasi Lender")

    if "investment_amount" in filtered_df.columns:
        total_investment = filtered_df["investment_amount"].sum()
        total_transactions = filtered_df["id_lender"].count()

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Investasi", f"Rp {total_investment:,.0f}")
        col2.metric("🔄 Total Transaksi", total_transactions)

        # ✅ Gunakan styler hanya jika diperlukan
        st.dataframe(
            filtered_df.style.format({"investment_amount": "Rp {:,.0f}"}),
            use_container_width=True
        )
    else:
        st.error("⚠️ Kolom 'investment_amount' tidak ditemukan dalam data!")

# ============================
# 📈 Halaman Grafik Investasi
# ============================
elif page == "Grafik Investasi Lender":
    st.header("📈 Grafik Investasi Lender")

    if not filtered_df.empty and "investment_amount" in filtered_df.columns:
        fig = px.bar(
            filtered_df,
            x="investment_date",
            y="investment_amount",
            color="id_lender",
            title="Tren Investasi per Lender",
            labels={
                "investment_date": "Tanggal Investasi",
                "investment_amount": "Jumlah Investasi"
            }
        )
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ Data tidak tersedia atau kolom 'investment_amount' tidak ditemukan untuk filter yang dipilih.")
