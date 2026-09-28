import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# 1. Fungsi Koneksi ke Database MySQL
def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_dal'
    )
    return connection

# 2. Fungsi Mengambil Data dari DB
def get_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM pddikti_example"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Judul Aplikasi
st.title('Streamlit Simple App')

# Sidebar Navigasi (Cukup panggil satu kali di sini)
page = st.sidebar.radio("Pilih Halaman", ["Dataset", "Visualisasi", "Form Input"])

# Ambil Data dari Database
data = get_data_from_db()

# Halaman 1: Dataset
if page == "Dataset":
    st.header("Halaman Dataset")
    st.dataframe(data)

# Halaman 2: Visualisasi
elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
    
    # Dropdown Pilih Universitas
    list_univ = data['universitas'].unique()
    selected_univ = st.selectbox("Pilih Universitas", list_univ)
    
    # Filter Data berdasarkan Universitas yang dipilih
    filtered_data = data[data['universitas'] == selected_univ]
    
    # Membuat Line Chart Visualisasi Data
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for prodi in filtered_data['program_studi'].unique():
        prodi_data = filtered_data[filtered_data['program_studi'] == prodi]
        ax.plot(prodi_data['semester'], prodi_data['jumlah'], label=prodi)
        
    ax.set_title(f"Visualisasi Data untuk {selected_univ}")
    ax.set_xlabel("Semester")
    ax.set_ylabel("Jumlah")
    plt.xticks(rotation=90)
    ax.legend()
    
    # Tampilkan Grafik
    st.pyplot(fig)

# Halaman 3: Form Input
elif page == "Form Input":
    st.header("Halaman Form Input")
    
    # Membuat Form dan Tombol Submit dalam satu blok
    with st.form(key='input_form'):
        input_semester = st.text_input('Semester')
        input_jumlah = st.number_input('Jumlah', min_value=0, format='%d')
        input_program_studi = st.text_input('Program Studi')
        input_universitas = st.text_input('Universitas')
        submit_button = st.form_submit_button(label='Submit Data')

        # Logika ketika tombol submit ditekan
        if submit_button:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO pddikti_example(semester, jumlah, program_studi, universitas)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (input_semester, input_jumlah, input_program_studi, input_universitas))
            conn.commit()
            conn.close()
            st.success("Data successfully submitted to the database!")