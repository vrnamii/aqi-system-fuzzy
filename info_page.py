import streamlit as st
import pandas as pd


def show_info_page():
    # Judul dengan styling
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: 32px; color: #1E88E5;'>
            Sistem Indeks Kualitas Udara (AQI)
        </h1>
    """,
        unsafe_allow_html=True,
    )

    # Penjelasan Sistem dengan layout yang lebih baik
    st.subheader("Tentang Sistem AQI")

    st.write(
            """
        Sistem Indeks Kualitas Udara (AQI) adalah sistem yang digunakan untuk mengukur dan 
        melaporkan tingkat polusi udara. Sistem ini menggunakan metode Fuzzy Logic dengan 
        mempertimbangkan 6 parameter polutan utama:
        """
        )


    # Parameter dengan ikon
    st.markdown(
        """
    | Ikon | Parameter | Keterangan |
    |------|-----------|------------|
    | 🔹 | **PM2.5** | Particulate Matter ≤ 2.5 µm |
    | 🔸 | **PM10** | Particulate Matter ≤ 10 µm |
    | 💨 | **CO** | Karbon Monoksida |
    | 🌫️ | **NO2** | Nitrogen Dioksida |
    | 🌤️ | **O3** | Ozon |
    | ⚡ | **SO2** | Sulfur Dioksida |
    """
    )

    # Tabel Kategori dengan styling yang lebih baik
    st.markdown('<h3 style="margin-top: 24px; margin-bottom: 0px;">Kategori Kualitas Udara</h3>', unsafe_allow_html=True)
    data = {
        "Kategori": [
            "Baik",
            "Sedang",
            "Buruk",
            "Tidak Sehat",
            "Sangat Tidak Sehat",
            "Berbahaya",
        ],
        "Rentang AQI": ["0-50", "50-100", "100-150", "150-200", "200-250", "250->300"],
        "Penjelasan": [
            "Kualitas udara memuaskan dan polusi udara menimbulkan risiko kecil atau tidak ada risiko.",
            "Kualitas udara dapat diterima namun beberapa polutan dapat menimbulkan masalah kesehatan ringan bagi sebagian kecil orang yang sangat sensitif.",
            "Anggota kelompok sensitif mungkin mengalami dampak kesehatan. Masyarakat umum cenderung tidak terpengaruh.",
            "Setiap orang mungkin mulai mengalami dampak kesehatan; anggota kelompok sensitif mungkin mengalami dampak kesehatan yang lebih serius.",
            "Peringatan kesehatan yang mengindikasikan bahwa setiap orang dapat mengalami dampak kesehatan yang lebih serius.",
            "Peringatan kesehatan darurat. Seluruh populasi kemungkinan terkena dampak.",
        ],
        "Rekomendasi": [
            "Lakukan aktivitas di luar ruangan seperti biasa",
            "Kurangi aktivitas fisik yang berkepanjangan di luar ruangan bagi kelompok sensitif",
            "Kurangi aktivitas fisik yang berkepanjangan di luar ruangan",
            "Hindari aktivitas fisik yang berkepanjangan di luar ruangan",
            "Hindari semua aktivitas fisik di luar ruangan",
            "Tetap di dalam ruangan dan tutup semua jendela",
        ],
    }

    df = pd.DataFrame(data)

    # Styling yang lebih modern
    st.markdown(
        """
    <style>
    .dataframe {
        font-size: 14px !important;
        border-collapse: collapse !important;
        width: 100% !important;
    }
    .dataframe th {
        background-color: #1E88E5 !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    .dataframe td {
        padding: 8px !important;
        border: 1px solid #ddd !important;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f9f9f9 !important;
    }
    .dataframe tr:hover {
        background-color: #f5f5f5 !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Menampilkan tabel dengan warna yang sesuai
    st.dataframe(
        df.style.apply(
            lambda x: [
                (
                    "background-color: #9EFF9E; color: black"
                    if x.name == 0
                    else (
                        "background-color: #FFFF9E; color: black"
                        if x.name == 1
                        else (
                            "background-color: #FFB84D; color: black"
                            if x.name == 2
                            else (
                                "background-color: #FF9E9E; color: black"
                                if x.name == 3
                                else (
                                    "background-color: #FF69B4; color: white"
                                    if x.name == 4
                                    else "background-color: #FF4D4D; color: white"
                                )
                            )
                        )
                    )
                )
                for i in range(len(x))
            ],
            axis=1,
        )
    )

    # Informasi Parameter Polutan dengan tabs
    st.markdown('<h3 style="margin-top: 24px; margin-bottom: 0px;">Informasi Parameter Polutan</h3>', unsafe_allow_html=True)

    tabs = st.tabs(["PM2.5", "PM10", "CO", "NO2", "O3", "SO2"])

    with tabs[0]:
        st.markdown(
            "<h6>PM10 (Particulate Matter ≤ 2.5 µm)</h6>",
            unsafe_allow_html=True
            )
        
        st.markdown(
            """
            - **Definisi**: Partikel halus dengan diameter 2.5 mikrometer atau lebih kecil
            - **Sumber**: Pembakaran, kendaraan bermotor, industri
            - **Dampak**: Dapat masuk ke dalam paru-paru dan aliran darah
            """
            )

    with tabs[1]:
        st.markdown(
            "<h6>PM10 (Particulate Matter ≤ 10 µm)</h6>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            - **Definisi**: Partikel dengan diameter 10 mikrometer atau lebih kecil
            - **Sumber**: Debu jalan, konstruksi, industri
            - **Dampak**: Dapat mengganggu sistem pernapasan
            """
            )

    with tabs[2]:
        st.markdown(
            "<h6>CO (Karbon Monoksida)</h6>",
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            - **Definisi**: Gas tidak berwarna dan tidak berbau
            - **Sumber**: Kendaraan bermotor, pembakaran tidak sempurna
            - **Dampak**: Mengurangi kemampuan darah mengangkut oksigen
            """
            )

    with tabs[3]:
        st.markdown(
            "<h6>NO2 (Nitrogen Dioksida)</h6>",
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            - **Definisi**: Gas berwarna kecoklatan dan berbau tajam
            - **Sumber**: Kendaraan bermotor, pembangkit listrik
            - **Dampak**: Iritasi saluran pernapasan, memperburuk asma
            """
            )

    with tabs[4]:
        st.markdown(
            "<h6>O3 (Ozon)</h6>",
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            - **Definisi**: Gas tidak berwarna dengan bau tajam
            - **Sumber**: Reaksi kimia polutan di udara dengan sinar matahari
            - **Dampak**: Iritasi mata dan saluran pernapasan, memperburuk asma
            """
            )

    with tabs[5]:
        st.markdown(
            "<h6>SO2 (Sulfur Dioksida)</h6>",
            unsafe_allow_html=True
        )
        
        st.markdown(
                """
            - **Definisi**: Gas tidak berwarna dengan bau tajam
            - **Sumber**: Pembangkit listrik, industri, kendaraan diesel
            - **Dampak**: Iritasi saluran pernapasan, memperburuk asma
            """
            )

    # Footer
    st.markdown(
    """
    <style>
        footer {
            visibility: hidden;
        }
        .footer-content {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            background-color: white;
            padding: 10px 0;
            color: gray;
            font-size: 14px;
        }
    </style>
    <div class="footer-content">
        Untuk pemantauan kualitas udara yang lebih baik 💙
    </div>
    """,
    unsafe_allow_html=True,
)
