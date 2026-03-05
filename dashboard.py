import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Fungsi untuk memuat dan membersihkan data
@st.cache_data
def load_data():

    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    # Ubah tipe data datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    # Mapping nilai kategorikal
    season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_mapping = {1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'}
    workingday_mapping = {0: 'Holiday/Weekend', 1: 'Working Day'}

    day_df['season'] = day_df['season'].map(season_mapping)
    day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)
    hour_df['workingday'] = hour_df['workingday'].map(workingday_mapping)

    return day_df, hour_df

day_df, hour_df = load_data()

# SIDEBAR UNTUK FILTER
st.sidebar.title("Bike Sharing Analytics")
st.sidebar.markdown("---")

# Filter rentang waktu
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Terapkan filter ke dataframe
filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# HALAMAN UTAMA (MAIN PAGE)
st.title("Bike Sharing Data Dashboard")
st.markdown("Visualisasi ini interaktif, silakan gunakan filter di sidebar untuk menyesuaikan rentang waktu.")
st.markdown("---")

# Row 1: Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Semua)", f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Total Pengguna Kasual", f"{filtered_day_df['casual'].sum():,}")
with col3:
    st.metric("Total Pengguna Terdaftar", f"{filtered_day_df['registered'].sum():,}")

st.markdown("---")

# Row 2: Visualisasi Pertanyaan 1 (Cuaca & Musim)
st.subheader("Pengaruh Kondisi Cuaca dan Musim terhadap Penyewaan")
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

sns.barplot(x='weathersit', y='cnt', data=filtered_day_df, errorbar=None, palette="Blues_d", ax=ax[0])
ax[0].set_title('Rata-rata Penyewaan Berdasarkan Cuaca', fontsize=14)
ax[0].set_xlabel('Kondisi Cuaca', fontsize=12)
ax[0].set_ylabel('Rata-rata Penyewaan', fontsize=12)
ax[0].tick_params(axis='x', rotation=15)

sns.barplot(x='season', y='cnt', data=filtered_day_df, errorbar=None, palette="Greens_d", ax=ax[1])
ax[1].set_title('Rata-rata Penyewaan Berdasarkan Musim', fontsize=14)
ax[1].set_xlabel('Musim', fontsize=12)
ax[1].set_ylabel('Rata-rata Penyewaan', fontsize=12)

st.pyplot(fig)

st.markdown("---")

# Row 3: Visualisasi Pertanyaan 2 (Tren per Jam)
st.subheader("Pola Penyewaan Sepeda: Hari Kerja vs Libur/Akhir Pekan")
fig2, ax2 = plt.subplots(figsize=(14, 6))

sns.lineplot(x='hr', y='cnt', hue='workingday', data=filtered_hour_df, errorbar=None, marker='o', palette='Set1', ax=ax2)
ax2.set_title('Tren Penyewaan Berdasarkan Jam', fontsize=16)
ax2.set_xlabel('Jam (0-23)', fontsize=12)
ax2.set_ylabel('Rata-rata Jumlah Sewa', fontsize=12)
ax2.set_xticks(range(0, 24))
ax2.grid(True, alpha=0.3)
ax2.legend(title='Tipe Hari')

st.pyplot(fig2)

st.caption("Dashboard Analytics oleh Mahdy")