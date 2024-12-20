import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/e2/Bangkit-logo.png" style="width: 45%;">
            <img src="https://images.tokopedia.net/img/FZfiOH/2021/6/11/20464998-9916-4493-b26d-42300122eb4e.png" style="width: 45%;">
        </div>
        """, unsafe_allow_html=True)
    st.title("Submission Belajar Analisis Data Dengan Python")    
    st.subheader("Name: Amanda F O Rakhmad")
    st.subheader("Student ID: M180B4KX0452")
    st.subheader("Dicoding ID: amandarakhmad")

st.title("Dashboard Air Quality Index Station Shunyi")

# Load datasets
data_O3 = pd.read_csv("Pertanyaan 1.csv")
data_NO2_O3 = pd.read_csv("Pertanyaan 2.csv")
korelasi_NO2_O3 = pd.read_csv("Pertanyaan 3.csv")

# Sidebar filters
with st.sidebar: 
    year_options = ['All'] + list(data_O3['tahun'].unique())
    selected_year = st.selectbox("Atur Tren Konsertrasi O3 Berdasarkan Tahun:", options=year_options)
    
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_mapping = {i + 1: month_labels[i] for i in range(12)}
    selected_months = st.multiselect(
        "Atur sesuai bulan (Optional)", 
        options=range(1, 13), 
        format_func=lambda x: month_mapping[x],  # Display month names in the multiselect
        default=range(1, 13)  # Default: Show all months
    )

# Filter data based on selected months and year
filtered_data = data_O3[data_O3['bulan'].isin(selected_months)]
if selected_year != 'All':
    filtered_data = filtered_data[filtered_data['tahun'] == int(selected_year)]

# Data Visualization - O3 Concentration Trends
st.title("Tren Konsentrasi O3 per Bulan tahun 2013-2017")
plt.figure(figsize=(12, 6))

# Plot data for the selected year and months
for year in filtered_data['tahun'].unique():
    subset = filtered_data[filtered_data['tahun'] == year]
    plt.plot(subset['bulan'], subset['nilai_rata_rata_per_bulan'], marker='o', label=str(year))

plt.title('Tren Konsentrasi O3 per Bulan (2013-2017)', fontsize=16)
plt.xlabel('Bulan', fontsize=14)
plt.ylabel('Konsentrasi O3', fontsize=14)
plt.xticks(
    ticks=range(1, 13),
    labels=month_labels
)
plt.legend(title='Tahun')
plt.grid(alpha=0.5)

st.pyplot(plt)

# Show scrollable table for the filtered data
st.write("Data Konsentrasi O3 Per Bulan Tahun Pemantauan 2013-2017:")

# Adding a container with scrollable functionality for the table
st.markdown("""
    <style>
    .dataframe-container {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #e1e1e1;
    }
    </style>
""", unsafe_allow_html=True)

# Using markdown to add the table with a fixed scrollable container
with st.container():
    table_html = filtered_data.to_html(classes='dataframe', index=False)
    st.markdown(f'<div class="dataframe-container">{table_html}</div>', unsafe_allow_html=True)

with st.expander("Interpretasi Data"):
    st.write("Tren Konsentrasi O3 di stasiun Shunyi dengan unit pengamatan rata-rata konsentrasi O3 per bulan pada tahun 2013 sampai 2017 mengalami kenaikan di setiap tahunnya. Grafik tren menunjukkan pola kenaikan di sekitar bulan Mei, Juni, dan Juli.")

# Visualization of average values for NO2 and O3 (2017)
mean_o3 = data_NO2_O3['O3'].mean()
mean_no2 = data_NO2_O3['NO2'].mean()

categories = ['O3', 'NO2']
values = [mean_o3, mean_no2]

st.title("Perbandingan Rata-Rata Konsentrasi O3 dan NO2 Tahun 2017")
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(categories, values, color=['skyblue', 'orange'])

ax.set_title("Rata-Rata Konsentrasi O3 dan NO2 (Tahun 2017)", fontsize=16)
ax.set_ylabel("Rata-Rata Konsentrasi", fontsize=14)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Interpretasi Data"):
    st.write("Perbandingan rata-rata konsentrasi O3 dan NO2 pada tahun 2017 menunjukkan bahwa nilai NO2 lebih besar daripada nilai O3.")

# Heatmap for correlation data
st.title("Uji Korelasi Antara Konsentrasi NO2 dengan O3")
correlation_matrix = korelasi_NO2_O3.corr()

st.write("Correlation Matrix:")
st.write(correlation_matrix)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Heatmap of Correlation Matrix", fontsize=16)
st.pyplot(fig)

with st.expander("Interpretasi Data"):
    st.write("Korelasi antara NO2 dan O3 menunjukkan hubungan negatif yang kuat dengan nilai -0,76. Hal ini menunjukkan apabila saat konsentrasi NO2 meningkat, maka konsentrasi O3 cenderung menurun dan sebaliknya.")
