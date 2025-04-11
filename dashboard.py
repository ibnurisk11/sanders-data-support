import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membaca data
df_personal_loan = pd.read_csv("daily-report-personal-20250410.csv")

# Konversi kolom "Tgl Disbursed" ke format datetime
df_personal_loan["Tgl Disbursed"] = pd.to_datetime(df_personal_loan["Tgl Disbursed"], format="%d/%m/%Y", errors='coerce')

# Filter hanya perusahaan yang diizinkan
allowed_companies = [
    "PT. Kaldu Sari Nabati", "PT. Pinus Merah Abadi", "PT. Richeese Kuliner Indonesia",
    "PT. Kieber Propertindo", "PT. Enerlife Indonesia", "PT. Satustop Finansial Solusi (Sanders)",
    "PT. Nutribev Nabati Indonesia", "PT. Nutribev Synergi Indonesia"
]
df_personal_loan = df_personal_loan[df_personal_loan["Borrower Name Company"].isin(allowed_companies)]

# Filter hanya marketing yang masih ada
allowed_marketers = [
    "Darsono", "Aditya Haryono", "Milda Noviyana", "Rizki Sitti Rachmawati", "Mentari Kusmana Dewi", "Risma Julianti",
    "Ajeng Nurul Siti Fatimah", "Fahira Rahmi Nur Awaliah",
]
# Filter hanya marketing yang masih ada atau nilai kosong
df_personal_loan = df_personal_loan[
    (df_personal_loan["Nama Marketing"].isin(allowed_marketers)) |
    (df_personal_loan["Nama Marketing"].isna())  # Menambahkan data yang kosong
]

# Navigasi
page = st.sidebar.radio("Navigasi", ["Data Terfilter", "Grafik Loan Status", "Grafik Capaian Marketing"])

# Sidebar Filter
st.sidebar.header("Filter Data")

# Dropdown untuk perusahaan
companies = ["Semua Perusahaan"] + list(df_personal_loan["Borrower Name Company"].dropna().unique())
selected_company = st.sidebar.selectbox("Pilih Perusahaan Borrower", companies)

# Dropdown untuk marketing
marketers = ["Semua Marketing"] + list(df_personal_loan["Nama Marketing"].dropna().unique())
selected_marketing = st.sidebar.selectbox("Pilih Nama Marketing", marketers)

# Dropdown untuk Loan Status
loan_statuses = ["Semua Status"] + list(df_personal_loan["Loan Status"].dropna().unique())
selected_status = st.sidebar.selectbox("Pilih Loan Status", loan_statuses)

# Filter berdasarkan tanggal
min_date = df_personal_loan["Tgl Disbursed"].min().date()
max_date = df_personal_loan["Tgl Disbursed"].max().date()
selected_dates = st.sidebar.date_input("Pilih Rentang Tanggal Disbursed", [min_date, max_date])
selected_dates = [pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])]

# Filter data
filtered_df = df_personal_loan[
    ((df_personal_loan["Borrower Name Company"] == selected_company) | (selected_company == "Semua Perusahaan")) &
    ((df_personal_loan["Nama Marketing"] == selected_marketing) | (selected_marketing == "Semua Marketing")) &
    ((df_personal_loan["Loan Status"] == selected_status) | (selected_status == "Semua Status")) &
    (df_personal_loan["Tgl Disbursed"] >= selected_dates[0]) &
    (df_personal_loan["Tgl Disbursed"] <= selected_dates[1])
]

# Kolom yang ditampilkan
selected_columns = [
    "Register Code", "Id Borrower Loan", "Bio Fullname",
    "Pinjaman", "Tenor", "Loan Note",
    "Borrower Name Company", "Nama Marketing", "Tgl Disbursed", "Loan Status"
]
filtered_df = filtered_df[selected_columns]

# Menampilkan Data Terfilter
if page == "Data Terfilter":
    st.header("📊 Data Loan Terfilter")

    # Statistik Tambahan
    total_loan_amount = filtered_df["Pinjaman"].sum()
    total_loan_count = filtered_df["Id Borrower Loan"].nunique()

    col1, col2 = st.columns(2)
    col1.metric("💰 Jumlah Pinjaman Didanai", f"Rp {total_loan_amount:,.0f}")
    col2.metric("📄 Jumlah Loan", total_loan_count)

    st.dataframe(filtered_df, use_container_width=True)

# Grafik Loan Status
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

    # Pie Chart
    st.header("📊 Persentase Loan Status per Marketing")
    loan_marketing_counts = filtered_df.groupby(["Nama Marketing", "Loan Status"])["Id Borrower Loan"].count().unstack()
    fig, ax = plt.subplots(figsize=(8, 8))
    loan_marketing_counts.sum(axis=1).plot(kind="pie", autopct='%1.1f%%', ax=ax)
    ax.set_title("Persentase Loan Status per Marketing")
    ax.set_ylabel("")
    st.pyplot(fig)

# Grafik Capaian Marketing
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