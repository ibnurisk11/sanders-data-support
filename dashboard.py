import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membaca data
df_personal_loan = pd.read_csv("daily-report-personal-20250325.csv")

# Konversi kolom "Tgl Disbursed" ke format datetime dengan format yang sesuai
df_personal_loan["Tgl Disbursed"] = pd.to_datetime(df_personal_loan["Tgl Disbursed"], format="%d/%m/%Y", errors='coerce')

# **Filter hanya perusahaan yang diizinkan**
allowed_companies = [
    "PT. Kaldu Sari Nabati", "PT. Pinus Merah Abadi", "PT. Richeese Kuliner Indonesia",
    "PT. Kieber Propertindo", "PT. Enerlife Indonesia", "PT. Satustop Finansial Solusi (Sanders)",
    "PT. Nutribev Nabati Indonesia", "PT. Nutribev Synergi Indonesia"
]

df_personal_loan = df_personal_loan[df_personal_loan["Borrower Name Company"].isin(allowed_companies)]

# **Navigasi Dashboard**
page = st.sidebar.radio("Navigasi", ["Data Terfilter", "Grafik Loan Status", "Grafik Capaian Marketing"])

# **Menampilkan filter di sidebar**
st.sidebar.header("Filter Data")

# **Dropdown untuk memilih Borrower Name Company (dengan opsi "Semua Perusahaan")**
companies = ["Semua Perusahaan"] + list(df_personal_loan["Borrower Name Company"].dropna().unique())
selected_company = st.sidebar.selectbox("Pilih Perusahaan Borrower", companies)

# **Dropdown untuk memilih Nama Marketing (dengan opsi "Semua Marketing")**
marketers = ["Semua Marketing"] + list(df_personal_loan["Nama Marketing"].dropna().unique())
selected_marketing = st.sidebar.selectbox("Pilih Nama Marketing", marketers)

# **Filter berdasarkan "Tgl Disbursed"**
min_date = df_personal_loan["Tgl Disbursed"].min().date()
max_date = df_personal_loan["Tgl Disbursed"].max().date()
selected_dates = st.sidebar.date_input("Pilih Rentang Tanggal Disbursed", [min_date, max_date])

# **Konversi tanggal dari date ke datetime64[ns] untuk kompatibilitas dengan DataFrame**
selected_dates = [pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])]

# **Filter data berdasarkan pilihan pengguna dan rentang tanggal**
filtered_df = df_personal_loan[
    ((df_personal_loan["Borrower Name Company"] == selected_company) | (selected_company == "Semua Perusahaan")) & 
    ((df_personal_loan["Nama Marketing"] == selected_marketing) | (selected_marketing == "Semua Marketing")) &
    (df_personal_loan["Tgl Disbursed"] >= selected_dates[0]) &
    (df_personal_loan["Tgl Disbursed"] <= selected_dates[1])
]

# Hanya menampilkan kolom yang diminta
selected_columns = [
    "Register Code", "Id Borrower Loan", "Bio Fullname",
    "Pinjaman", "Tenor", "Loan Note",
    "Borrower Name Company", "Nama Marketing", "Tgl Disbursed", "Loan Status"
]
filtered_df = filtered_df[selected_columns]

# **Menampilkan Data Terfilter**
if page == "Data Terfilter":
    st.header("📊 Data Loan Terfilter")
    st.dataframe(filtered_df, use_container_width=True)

# **Grafik Loan Status per Perusahaan**
elif page == "Grafik Loan Status":
    st.header("📈 Distribusi Loan Status per Perusahaan")

    loan_company_counts = filtered_df.groupby(["Borrower Name Company", "Loan Status"])["Id Borrower Loan"].count().unstack()
    fig, ax = plt.subplots(figsize=(10, 5))
    loan_company_counts.plot(kind="bar", stacked=True, ax=ax)

    ax.set_ylabel("Jumlah Id Borrower Loan")
    ax.set_xlabel("Nama Perusahaan")
    ax.set_title("Jumlah Loan Status per Perusahaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Grafik Pie: Loan Status berdasarkan Nama Marketing
    st.header("📊 Persentase Loan Status per Marketing")

    loan_marketing_counts = filtered_df.groupby(["Nama Marketing", "Loan Status"])["Id Borrower Loan"].count().unstack()
    fig, ax = plt.subplots(figsize=(8, 8))
    loan_marketing_counts.sum(axis=1).plot(kind="pie", autopct='%1.1f%%', ax=ax)
    
    ax.set_title("Persentase Loan Status per Marketing")
    ax.set_ylabel("")
    st.pyplot(fig)

# **Grafik Capaian Marketing dalam Bentuk Diagram Batang**
elif page == "Grafik Capaian Marketing":
    st.header("📊 Capaian Marketing berdasarkan Tanggal Disbursed")

    marketing_disbursed_counts = filtered_df.groupby(["Tgl Disbursed", "Nama Marketing"])["Id Borrower Loan"].count().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    marketing_disbursed_counts.plot(kind="bar", stacked=True, ax=ax)

    ax.set_ylabel("Jumlah Id Borrower Loan")
    ax.set_xlabel("Tanggal Disbursed")
    ax.set_title("Capaian Marketing berdasarkan Tanggal Disbursed")
    plt.xticks(rotation=45)
    st.pyplot(fig)