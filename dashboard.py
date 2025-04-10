import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membaca data
df_personal_loan = pd.read_csv("daily-report-personal-20250325.csv")

# Konversi kolom "Tgl Disbursed" ke format datetime dengan format yang sesuai
df_personal_loan["Tgl Disbursed"] = pd.to_datetime(df_personal_loan["Tgl Disbursed"], format="%d/%m/%Y", errors='coerce')

# Menampilkan filter di sidebar
st.sidebar.header("Filter Data")

# **Dropdown untuk memilih Borrower Name Company (dengan opsi "Semua Perusahaan")**
companies = ["Semua Perusahaan"] + list(df_personal_loan["Borrower Name Company"].dropna().unique())
selected_company = st.sidebar.selectbox("Pilih Perusahaan Borrower", companies)

# Dropdown untuk memilih Nama Marketing
marketers = df_personal_loan["Nama Marketing"].dropna().unique()
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
    (df_personal_loan["Nama Marketing"] == selected_marketing) &
    (df_personal_loan["Tgl Disbursed"] >= selected_dates[0]) &
    (df_personal_loan["Tgl Disbursed"] <= selected_dates[1])
]

# Hanya menampilkan kolom yang diminta
selected_columns = [
    "Register Code", "Id Borrower Loan", "Bio Fullname",
    "Pinjaman", "Tenor", "Loan Note",
    "Borrower Name Company", "Nama Marketing", "Tgl Disbursed"
]
filtered_df = filtered_df[selected_columns]

# Menampilkan DataFrame hasil filter
st.header("Data Loan Terfilter")
st.dataframe(filtered_df, use_container_width=True)

# **Menghitung jumlah "Id Borrower Loan" berdasarkan "Tgl Disbursed" dalam rentang yang dipilih**
loan_disbursed_counts = filtered_df.groupby("Tgl Disbursed")["Id Borrower Loan"].count().reset_index()

# **Membuat visualisasi dengan Matplotlib**
st.subheader(f"Pinjaman telah cair untuk {selected_company} - {selected_marketing} ({selected_dates[0].date()} hingga {selected_dates[1].date()})")
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(loan_disbursed_counts["Tgl Disbursed"], loan_disbursed_counts["Id Borrower Loan"], marker='o', linestyle='-')

ax.set_ylabel("Jumlah Borrower Loan")
ax.set_xlabel("Tanggal Disbursed")
ax.set_title(f"Capaian Pinjaman Cair - {selected_company}")

plt.xticks(rotation=45)
st.pyplot(fig)