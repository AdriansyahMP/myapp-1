import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

df_day = pd.read_csv('submission/day_cleaned.csv')
df_day['dateday'] = pd.to_datetime(df_day['dateday'])

st.title('🚲 Bike Sharing Dashboard')
st.write('Dashboard ini menampilkan analisis data penyewaan sepeda')

st.sidebar.title('About')
st.sidebar.info('Dashboard ini dibuat oleh Adriansyah Maulana Putra')

tab1, tab2, tab3 = st.tabs(['Daily Pattern', 'Seasonal Pattern', 'Trend Analysis'])

with tab1:
    st.header('1. Analisis Pola Harian')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Rata-rata Penyewaan per Hari')
        daily_avg = df_day.groupby('weekday')['count'].mean().round(2)
        st.bar_chart(daily_avg)
        
    with col2:
        st.subheader('Distribusi Penyewaan per Hari')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_day, x='weekday', y='count')
        plt.xticks(rotation=45)
        plt.xlabel('Hari')
        plt.ylabel('Jumlah Penyewaan')
        st.pyplot(fig)
        plt.close()

with tab2:
    st.header('2. Analisis Pola Musiman')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Rata-rata Penyewaan per Musim')
        seasonal_avg = df_day.groupby('season')['count'].mean().round(2)
        st.bar_chart(seasonal_avg)
        
    with col2:
        st.subheader('Pengaruh Cuaca terhadap Penyewaan')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_day, x='weather_category', y='count')
        plt.xticks(rotation=45)
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Jumlah Penyewaan')
        st.pyplot(fig)
        plt.close()
    
    st.subheader('Tren Penyewaan per Musim')
    fig, ax = plt.subplots(figsize=(15, 6))
    for season in df_day['season'].unique():
        season_data = df_day[df_day['season'] == season]
        ax.plot(season_data['dateday'], season_data['count'], label=season, alpha=0.7)
    plt.legend()
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(fig)
    plt.close()

with tab3:
    st.header('3. Analisis Trend')
    
    st.subheader('Trend Penyewaan Sepanjang Waktu')
    
    min_date = df_day['dateday'].min()
    max_date = df_day['dateday'].max()
    
    date_range = st.date_input(
        "Pilih Rentang Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df_day['dateday'].dt.date >= start_date) & (df_day['dateday'].dt.date <= end_date)
        filtered_df = df_day.loc[mask]
        
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.plot(filtered_df['dateday'], filtered_df['count'], label='Daily Rentals')
        
        monthly_avg = filtered_df.resample('M', on='dateday')['count'].mean()
        ax.plot(monthly_avg.index, monthly_avg.values, 'r-', linewidth=2, label='Monthly Average')
        
        plt.legend()
        plt.xlabel('Tanggal')
        plt.ylabel('Jumlah Penyewaan')
        st.pyplot(fig)
        plt.close()
    
    st.subheader('Korelasi Faktor Cuaca dengan Penyewaan')
    
    corr_cols = ['count', 'temp', 'humidity', 'windspeed']
    corr_matrix = df_day[corr_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    st.pyplot(fig)
    plt.close()

st.header('Kesimpulan')
st.write("""
- Hari kerja menunjukkan pola penyewaan yang lebih tinggi dibanding akhir pekan, dengan puncak pada hari Kamis dan Jumat.
- Musim Fall (Gugur) memiliki jumlah penyewaan tertinggi, diikuti oleh Summer (Panas).
- Cuaca memiliki pengaruh signifikan terhadap jumlah penyewaan, dengan cuaca cerah menunjukkan jumlah penyewaan tertinggi.
- Terdapat trend peningkatan jumlah penyewaan dari tahun 2011 ke 2012.
""")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)