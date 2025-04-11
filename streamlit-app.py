import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Sidebar untuk filter rentang tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", value=pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("Tanggal Akhir", value=pd.to_datetime("2024-01-31"))

# Validasi rentang tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal Mulai tidak boleh lebih besar dari Tanggal Akhir.")
    st.stop()

# Query data berdasarkan rentang tanggal
query = f"""
    SELECT a.id_borrower_loan, a.register_code, b.bio_fullname, a.loan_status, a.loan_start_date
    FROM tb_fintech_borrower_loan a
    JOIN tb_fintech_borrower_bio b ON a.register_code = b.register_code
    WHERE DATE(a.loan_start_date) BETWEEN '{start_date}' AND '{end_date}';
"""
df_personal_loan = conn.query(query, ttl=600)

# Tampilkan data yang difilter
st.header("📋 Data Loan yang Difilter")
st.dataframe(df_personal_loan, use_container_width=True)

# Diagram Pie untuk Loan Status
st.header("📊 Diagram Pie Loan Status")
if not df_personal_loan.empty:
    loan_status_counts = df_personal_loan["loan_status"].value_counts().reset_index()
    loan_status_counts.columns = ["loan_status", "count"]

    fig = px.pie(
        loan_status_counts,
        names="loan_status",
        values="count",
        title="Distribusi Loan Status",
        hole=0.4
    )
    st.plotly_chart(fig)
else:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter.")