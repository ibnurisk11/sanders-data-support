import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Membaca data
df_payday_loan = pd.read_csv("data/daily-report-payday-20250410.csv")

# Konversi kolom "Tgl Disbursed" ke format datetime
df_payday_loan["Tgl Disbursed"] = pd.to_datetime(df_payday_loan["Tgl Disbursed"], format="%d/%m/%Y", errors='coerce')

# **Filter awal untuk hanya menampilkan data dengan Tgl Disbursed >= '2024-01-01'**
df_payday_loan = df_payday_loan[df_payday_loan["Tgl Disbursed"] >= "2024-01-01"]

# **Filter hanya perusahaan yang diizinkan**
allowed_companies = [
    "PT. Kaldu Sari Nabati", "PT. Pinus Merah Abadi", "PT. Richeese Kuliner Indonesia",
    "PT. Kieber Propertindo", "PT. Enerlife Indonesia", "PT. Satustop Finansial Solusi (Sanders)",
    "PT. Nutribev Nabati Indonesia", "PT. Nutribev Synergi Indonesia"
]
df_payday_loan = df_payday_loan[df_payday_loan["Borrower Name Company"].isin(allowed_companies)]

# **Filter hanya marketing yang masih ada atau nilai kosong**
allowed_marketers = [
    "Darsono", "Aditya Haryono", "Milda Noviyana", "Rizki Sitti Rachmawati", "Mentari Kusmana Dewi", "Risma Julianti",
    "Ajeng Nurul Siti Fatimah", "Fahira Rahmi Nur Awaliah",
]
df_payday_loan = df_payday_loan[
    (df_payday_loan["Nama Marketing"].isin(allowed_marketers)) |
    (df_payday_loan["Nama Marketing"].isna())  # Menambahkan data yang kosong
]

# **Navigasi Dashboard**
page = st.sidebar.radio("Navigasi", ["Data Terfilter", "Grafik Loan Status", "Grafik Capaian Marketing"])

# **Menampilkan filter di sidebar**
st.sidebar.header("Filter Data")

# **Dropdown untuk memilih Borrower Name Company**
companies = ["Semua Perusahaan"] + list(df_payday_loan["Borrower Name Company"].dropna().unique())
selected_company = st.sidebar.selectbox("Pilih Perusahaan Borrower", companies)

# **Dropdown untuk memilih Nama Marketing**
marketers = ["Semua Marketing"] + list(df_payday_loan["Nama Marketing"].dropna().unique())
selected_marketing = st.sidebar.selectbox("Pilih Nama Marketing", marketers)

# **Dropdown untuk Loan Status**
loan_statuses = ["Semua Status"] + list(df_payday_loan["Loan Status"].dropna().unique())
selected_status = st.sidebar.selectbox("Pilih Loan Status", loan_statuses)

# **Filter berdasarkan tanggal**
min_date = df_payday_loan["Tgl Disbursed"].min().date()
max_date = df_payday_loan["Tgl Disbursed"].max().date()
selected_dates = st.sidebar.date_input("Pilih Rentang Tanggal Disbursed", [min_date, max_date])
selected_dates = [pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])]

# Dropdown untuk Tenor
loan_tenor = ["Semua Tenor"] + list(df_payday_loan["Tenor"].dropna().unique())
selected_tenor = st.sidebar.selectbox("Pilih Tenor", loan_tenor)

# Tambahkan decorator @st.cache_data untuk caching
@st.cache_data
def filter_data(df, selected_company, selected_marketing, selected_status, selected_tenor, selected_dates):
    return df[
        ((df["Borrower Name Company"] == selected_company) | (selected_company == "Semua Perusahaan")) &
        ((df["Nama Marketing"] == selected_marketing) | (selected_marketing == "Semua Marketing")) &
        ((df["Loan Status"] == selected_status) | (selected_status == "Semua Status")) &
        ((df["Tenor"] == selected_tenor) | (selected_tenor == "Semua Tenor")) &
        (df["Tgl Disbursed"] >= selected_dates[0]) &
        (df["Tgl Disbursed"] <= selected_dates[1])
    ]

# Panggil fungsi filter_data
filtered_df = filter_data(
    df_payday_loan, selected_company, selected_marketing, selected_status, selected_tenor, selected_dates
)

# **Kolom yang ditampilkan**
selected_columns = [
    "Register Code", "Id Borrower Loan", "Bio Fullname",
    "Pinjaman", "Tenor", "Loan Note",
    "Borrower Name Company", "Nama Marketing", "Tgl Disbursed", "Loan Status"
]
filtered_df = filtered_df[selected_columns]

# **Menampilkan Data Terfilter**
if page == "Data Terfilter":
    st.header("📊 Data Loan Terfilter")

    # **Statistik Tambahan**
    total_loan_amount = filtered_df["Pinjaman"].sum()
    total_loan_count = filtered_df["Id Borrower Loan"].nunique()

    col1, col2 = st.columns(2)
    col1.metric("💰 Jumlah Pinjaman Didanai", f"Rp {total_loan_amount:,.0f}")
    col2.metric("📄 Jumlah Loan", total_loan_count)

    st.dataframe(filtered_df, use_container_width=True)

# **Grafik Loan Status**
elif page == "Grafik Loan Status":
    # Ganti bar chart Matplotlib dengan Plotly
    st.header("📈 Distribusi Loan Status per Perusahaan")
    loan_company_counts = filtered_df.groupby(["Borrower Name Company", "Loan Status"])["Id Borrower Loan"].count().unstack()
    fig = px.bar(
        loan_company_counts.reset_index(),
        x="Borrower Name Company",
        y=loan_company_counts.columns,
        title="Jumlah Loan Status per Perusahaan",
        labels={"value": "Jumlah Id Borrower Loan", "Borrower Name Company": "Nama Perusahaan"},
        barmode="stack"
    )
    st.plotly_chart(fig)

    st.header("📊 Persentase Loan Status per Marketing")
    loan_marketing_counts = filtered_df.groupby(["Nama Marketing", "Loan Status"])["Id Borrower Loan"].count().unstack()
    loan_marketing_counts["Total"] = loan_marketing_counts.sum(axis=1)
    fig = px.pie(
        loan_marketing_counts.reset_index(),
        values="Total",
        names="Nama Marketing",
        title="Persentase Loan Status per Marketing",
        hole=0.4
    )
    st.plotly_chart(fig)

# **Grafik Capaian Marketing**
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