import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Judul
st.title("Dashboard")
with st.sidebar:
    st.markdown("""
    - **Author:** Mochamad Yusuf
    - **Email:** mochyusuf100@gmail.com
    - **ID Dicoding:** mochyusuf
    """)

# Load Dataset
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")

# Ubah `dteday` menjadi waktu-tanggal
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_day['dteday'])

# Ekstrak tahun, bulan, dan hari dari `dteday` untuk df_day
df_day['year'] = df_day['dteday'].dt.year
df_day['month'] = df_day['dteday'].dt.month
df_day['day'] = df_day['dteday'].dt.day

# Ekstrak tahun, bulan, hari, dan jam dari `dteday` untuk df_hour
df_hour['year'] = df_hour['dteday'].dt.year
df_hour['month'] = df_hour['dteday'].dt.month
df_hour['day'] = df_hour['dteday'].dt.day
df_hour['hour'] = df_hour['dteday'].dt.hour

# Hitung rata-rata penyewaan per bulan
monthly_avg_rentals = df_day.groupby(df_day['dteday'].dt.month)['cnt'].mean().reset_index()
monthly_avg_rentals.columns = ['bulan', 'cnt']
monthly_avg_rentals.head()

# total terpinjam pada bulan Januari 2011
def create_total_pinjam(df_hour):
    total = df_hour[(df_hour['yr'] == 1) & (df_hour['mnth'] == 1)]['cnt'].sum()

    return "Total terpinjam pada bulan Januari 2011 : " + str(total)

# Menghitung Total terpinjam bulan Januari 2011 
total_pinjam = create_total_pinjam(df_hour)

# Menampilkan Total Pinjam
st.write(total_pinjam)

# Lihat Rata-Rata Jumlah Sepeda Per bulan dalam setahun
bulanan = monthly_avg_rentals.groupby(pd.Grouper(key='bulan')).sum()
fig = plt.figure(figsize=(12, 5))
plt.plot(bulanan.index, bulanan['cnt'],marker='o',linestyle='-')
plt.title('Rata-Rata Jumlah Sepeda per Bulan dalam setahun')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Sepeda')
plt.grid(True)
plt.show()

st.pyplot(fig)

# Hitung total keseluruhan dari 'casual' dan 'register'
total_casual = df_hour['casual'].sum()
total_register = df_hour['registered'].sum()

# Data
categories = ['Casual', 'Register']
totals = [total_casual, total_register]

# Buat chart
fig = plt.figure(figsize=(8, 6))
plt.bar(categories, totals, color=['blue', 'red'])

# Tambahkan label dan judul
plt.xlabel('User Type')
plt.ylabel('Total')
plt.title('Total Casual and Register Users')

# Tambahkan nilai di atas bar
for i, value in enumerate(totals):
    plt.text(i, value + 10000, f'{value:,}', ha='center', va='bottom')

# Tampilkan grafik
plt.show()

st.pyplot(fig)

# Menghitung jumlah pelanggan per bulan
monthly_counts = df_day.groupby(['year', 'month']).agg({
    'cnt': 'sum'
}).reset_index()

# Mengubah index bulan ke nomor bulan yang tepat, menambahkan kolom baru *month_num*
month_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
monthly_counts['month_num'] = monthly_counts['month'].apply(lambda x: month_order.index(x) + 1)

# Mengurutkan data berdasarkan tahun dan bulan
monthly_counts = monthly_counts.sort_values(by=['year', 'month_num'])

# Melakukan plotting
fig = plt.figure(figsize=(10, 5))
for year in monthly_counts['year'].unique():
    subset = monthly_counts[monthly_counts['year'] == year]
    plt.plot(subset['month'], subset['cnt'], marker='o', label=year)

plt.title('Tren Penyewaan Sepeda Selama tahun 2011, 2012')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Tahun')
plt.grid(True)

# Menampilkan chart
plt.show()

st.pyplot(fig)