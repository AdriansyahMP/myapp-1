import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read CSV data
data = pd.read_csv("C:/day.csv")

# Handle date column if necessary (replace 'dteday' with the actual name)
date_col = 'dteday'
if pd.api.types.is_string_dtype(data[date_col]):
    data[date_col] = pd.to_datetime(data[date_col])

# Function to calculate average bike rentals by weekday
def calculate_weekday_usage(df):
    return df.groupby('weekday')['cnt'].mean()

# Function to create a scatter plot with user-selected variable
def create_scatter_plot(df, x_variable):
    fig, ax = plt.subplots()
    sns.scatterplot(x=x_variable, y='cnt', data=df, ax=ax)
    return fig

# Main 
st.title('ADRIANSYAH MAULANA PUTRA')

# Display data overview
st.subheader('Analisis Data Sewa Sepeda')
st.write(data.info())

# Average bike rentals by weekday
weekday_usage = calculate_weekday_usage(data.copy())
st.subheader('Rata-Rata Sewa Sepeda per Hari Kerja')
st.dataframe(weekday_usage)

# Plot average bike rentals by weekday
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=weekday_usage.index, y=weekday_usage, ax=ax)
plt.xlabel('Weekday (0=Sunday, 6=Saturday)')
plt.ylabel('Average Bike Rentals')
plt.title('Average Bike Rentals by Weekday')
st.pyplot(fig)

# Correlation heatmap - Simple version
st.subheader('Korelasi Antar Fitur')

# Setup figure size and create a simpler heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(data.corr(), cmap='Blues', ax=ax)  # Simplified without annotations and with a basic color palette

# Display the heatmap
st.pyplot(fig)

# Scatter plot with user selection
selected_variable = st.selectbox('Pilih Variabel untuk Scatter Plot', ['temp', 'hum'])
fig = create_scatter_plot(data.copy(), selected_variable)
st.subheader(f'Scatter Plot: Sewa Sepeda vs {selected_variable}')
st.pyplot(fig)

# Additional insights (optional)

st.subheader('Kesimpulan Awal')
st.write("""
Berdasarkan data yang telah dianalisis, dapat disimpulkan bahwa:
- Pola Penggunaan: Penggunaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan akhir pekan. Ini menunjukkan bahwa banyak orang menggunakan sepeda sebagai alat transportasi sehari-hari.
- Pengaruh Cuaca: Cuaca, terutama suhu, memiliki pengaruh signifikan terhadap jumlah sewa sepeda. Cuaca yang hangat dan cerah cenderung meningkatkan minat bersepeda.
- Faktor Lain: Selain cuaca, faktor seperti hari libur, acara khusus, dan kebijakan pemerintah juga dapat mempengaruhi pola penggunaan sepeda.

**Rekomendasi**

Untuk analisis lebih lanjut dan pengembangan bisnis, disarankan:
- Visualisasi Interaktif: Gunakan alat visualisasi seperti Plotly untuk eksplorasi data yang lebih mendalam.
- Model Prediktif: Bangun model untuk memprediksi jumlah sewa berdasarkan berbagai faktor.
- Segmentasi Pengguna: Bagi pengguna berdasarkan karakteristik untuk pemahaman yang lebih spesifik.
""")
