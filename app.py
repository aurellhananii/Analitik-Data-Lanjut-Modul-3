import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analitik Data Lanjut",
    page_icon="📊",
    layout="wide"
)

st.title("Streamlit Simple App")
st.write("Aplikasi Analitik Data Lanjut")

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    data = load_data()
except Exception as e:
    st.error("File data.csv tidak ditemukan.")
    st.write(e)
    st.stop()

st.sidebar.title("Pilih Halaman")

halaman = st.sidebar.radio(
    "Pilih:",
    ["Dataset", "Visualisasi", "Form Input"]
)

# =========================
# DATASET
# =========================

if halaman == "Dataset":

    st.header("Dataset")

    st.dataframe(
        data,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Jumlah Baris",
            data.shape[0]
        )

    with col2:
        st.metric(
            "Jumlah Kolom",
            data.shape[1]
        )

# =========================
# VISUALISASI
# =========================

elif halaman == "Visualisasi":

    st.header("Visualisasi Data")

    kolom_numerik = data.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if len(kolom_numerik) == 0:

        st.warning("Tidak ada data numerik.")

    else:

        kolom = st.selectbox(
            "Pilih kolom:",
            kolom_numerik
        )

        fig = px.line(
            data,
            y=kolom,
            markers=True,
            title=f"Tren {kolom}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================
# FORM INPUT
# =========================

elif halaman == "Form Input":

    st.header("Form Input Data")

    st.write("Masukkan data baru.")

    kolom_numerik = data.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if len(kolom_numerik) > 0:

        with st.form("form_input"):

            nilai = {}

            for kolom in kolom_numerik:

                nilai[kolom] = st.number_input(
                    f"{kolom}",
                    value=0.0
                )

            submit = st.form_submit_button(
                "Tambah Data"
            )

        if submit:

            data_baru = pd.DataFrame([nilai])

            st.success("Data berhasil ditambahkan!")

            st.dataframe(
                data_baru,
                use_container_width=True
            )