import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from rules import create_rules
from info_page import show_info_page
import plotly.graph_objects as go

# Set page config at the very beginning
st.set_page_config(page_title="Sistem AQI", page_icon="🌬️", layout="wide")


@st.cache_resource
def initialize_fuzzy_system():
    """
    Initialize fuzzy system dengan cache untuk menghindari inisialisasi berulang
    """
    # 1. Definisi variabel input dan output
    pm25 = ctrl.Antecedent(np.arange(0, 446, 1), "PM2.5")
    pm10 = ctrl.Antecedent(np.arange(0, 551, 1), "PM10")
    co = ctrl.Antecedent(np.arange(0, 54166, 1), "CO")
    no2 = ctrl.Antecedent(np.arange(0, 551, 1), "NO2")
    o3 = ctrl.Antecedent(np.arange(0, 1502, 1), "O3")
    so2 = ctrl.Antecedent(np.arange(0, 3001, 1), "SO2")
    aqi = ctrl.Consequent(np.arange(0, 551, 1), "AQI")

    # 2. Definisi fungsi keanggotaan (membership functions)
    pm25["baik"] = fuzz.trapmf(pm25.universe, [0, 0, 15, 45])
    pm25["sedang"] = fuzz.trimf(pm25.universe, [15, 45, 75])
    pm25["buruk"] = fuzz.trimf(pm25.universe, [45, 75, 105])
    pm25["tidak_sehat"] = fuzz.trimf(pm25.universe, [75, 105, 135])
    pm25["parah"] = fuzz.trimf(pm25.universe, [105, 185, 265])
    pm25["berbahaya"] = fuzz.trapmf(pm25.universe, [185, 315, 445, 445])

    # PM10
    pm10["baik"] = fuzz.trapmf(pm10.universe, [0, 0, 25, 75])
    pm10["sedang"] = fuzz.trimf(pm10.universe, [25, 75, 125])
    pm10["buruk"] = fuzz.trimf(pm10.universe, [75, 175, 275])
    pm10["tidak_sehat"] = fuzz.trimf(pm10.universe, [210, 300, 390])
    pm10["parah"] = fuzz.trimf(pm10.universe, [310, 390, 470])
    pm10["berbahaya"] = fuzz.trapmf(pm10.universe, [390, 470, 550, 550])

    # CO
    co["baik"] = fuzz.trapmf(co.universe, [0, 0, 4165, 12500])
    co["sedang"] = fuzz.trimf(co.universe, [4165, 12500, 20835])
    co["buruk"] = fuzz.trimf(co.universe, [12505, 20835, 29165])
    co["tidak_sehat"] = fuzz.trimf(co.universe, [20835, 29165, 37495])
    co["parah"] = fuzz.trimf(co.universe, [29165, 37500, 45835])
    co["berbahaya"] = fuzz.trapmf(co.universe, [37505, 45835, 54165, 54165])

    # NO2
    no2["baik"] = fuzz.trapmf(no2.universe, [0, 0, 20, 60])
    no2["sedang"] = fuzz.trimf(no2.universe, [20, 60, 100])
    no2["buruk"] = fuzz.trimf(no2.universe, [75, 130, 185])
    no2["tidak_sehat"] = fuzz.trimf(no2.universe, [130, 185, 240])
    no2["parah"] = fuzz.trimf(no2.universe, [185, 295, 405])
    no2["berbahaya"] = fuzz.trapmf(no2.universe, [350, 450, 550, 550])

    # O3
    o3["baik"] = fuzz.trapmf(o3.universe, [0, 0, 25, 75])
    o3["sedang"] = fuzz.trimf(o3.universe, [25, 75, 100])
    o3["buruk"] = fuzz.trimf(o3.universe, [80, 134, 188])
    o3["tidak_sehat"] = fuzz.trimf(o3.universe, [148, 188, 228])
    o3["parah"] = fuzz.trimf(o3.universe, [188, 470, 752])
    o3["berbahaya"] = fuzz.trapmf(o3.universe, [497, 999, 1501, 1501])

    # SO2
    so2["baik"] = fuzz.trapmf(so2.universe, [0, 0, 20, 60])
    so2["sedang"] = fuzz.trimf(so2.universe, [20, 60, 100])
    so2["buruk"] = fuzz.trimf(so2.universe, [60, 230, 400])
    so2["tidak_sehat"] = fuzz.trimf(so2.universe, [230, 590, 950])
    so2["parah"] = fuzz.trimf(so2.universe, [590, 1200, 1810])
    so2["berbahaya"] = fuzz.trapmf(so2.universe, [1200, 2100, 3000, 3000])

    # AQI Output
    aqi["baik"] = fuzz.trapmf(aqi.universe, [0, 0, 25, 75])
    aqi["sedang"] = fuzz.trimf(aqi.universe, [25, 75, 125])
    aqi["buruk"] = fuzz.trimf(aqi.universe, [75, 125, 175])
    aqi["tidak_sehat"] = fuzz.trimf(aqi.universe, [125, 175, 225])
    aqi["parah"] = fuzz.trimf(aqi.universe, [175, 225, 275])
    aqi["berbahaya"] = fuzz.trapmf(aqi.universe, [225, 275, 325, 325])

    # 3. Create rules and control system
    rules = create_rules(pm25, pm10, co, no2, o3, so2, aqi)
    aqi_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(aqi_ctrl)


@st.cache_data
def get_category_color(aqi_value):
    """Cache function untuk mendapatkan warna dan kategori"""
    if aqi_value < 50:
        return "#9EFF9E", "Baik"
    elif aqi_value < 100:
        return "#FFFF9E", "Sedang"
    elif aqi_value < 150:
        return "#FFB84D", "Buruk"
    elif aqi_value < 200:
        return "#FF9E9E", "Tidak Sehat"
    elif aqi_value < 250:
        return "#FF69B4", "Parah"
    else:
        return "#FF4D4D", "Berbahaya"


@st.cache_data
def create_gauge_chart(value, title):
    """Cache function untuk membuat gauge chart"""
    color, _ = get_category_color(value)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title},
            gauge={
                "axis": {"range": [0, 300]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 50], "color": "#9EFF9E"},
                    {"range": [50, 100], "color": "#FFFF9E"},
                    {"range": [100, 150], "color": "#FFB84D"},
                    {"range": [150, 200], "color": "#FF9E9E"},
                    {"range": [200, 250], "color": "#FF69B4"},
                    {"range": [250, 300], "color": "#FF4D4D"},
                ],
            },
        )
    )
    fig.update_layout(height=300)
    return fig


def show_calculator_page():
    st.markdown(
        """
        <h1 style='text-align: center; color: #1E88E5; margin-bottom: 16px;'>
            Kalkulator AQI dengan Fuzzy Logic
        </h1>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='font-size: 16px; text-align: center;  margin-bottom: 40px;'>
            Masukkan nilai parameter polutan untuk menghitung Indeks Kualitas Udara
        </p>
    """,
        unsafe_allow_html=True,
    )

    # Initialize fuzzy system
    aqi_system = initialize_fuzzy_system()

    # Create two columns for input
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p style="font-size: 16px; font-weight: normal; margin-bottom: -40px;">PM2.5 (µg/m³)</p>', unsafe_allow_html=True)
        pm25_input = st.number_input(
            "",
            min_value=0,
            max_value=445,
            step=1,
            value=None,
            help="Particulate Matter ≤ 2.5 µm (Rentang nilai 0-380)",
        )

        st.markdown('<p style="font-size: 16px; font-weight: normal; margin-bottom: -40px;">CO (ppb)</p>', unsafe_allow_html=True)
        co_input = st.number_input(
            "",
            min_value=0,
            max_value=54165,
            step=1,
            value=None,
            help="Karbon Monoksida (Rentang nilai 0-8330)",
        )

        st.markdown('<p style="font-size: 16px; font-weight: normal; margin-bottom: -40px;">O3 (ppb)</p>', unsafe_allow_html=True)
        o3_input = st.number_input(
            "",
            min_value=0,
            max_value=1501,
            step=1,
            value=None,
            help="Ozon (Rentang nilai 0-80)",
        )

    with col2:
        st.markdown('<p style="font-size: 16px; font-weight: normal; margin-bottom: -40px;">PM10 (µg/m³)</p>', unsafe_allow_html=True)
        pm10_input = st.number_input(
            "",
            min_value=0,
            max_value=550,
            step=1,
            value=None,
            help="Particulate Matter ≤ 10 µm (Rentang nilai 0-510)",
        )

        st.markdown('<p style="font-size: 16px; font-weight: normal; margin-bottom: -40px;">NO2 (ppb)</p>', unsafe_allow_html=True)
        no2_input = st.number_input(
            "",
            min_value=0,
            max_value=550,
            step=1,
            value=None,
            help="Nitrogen Dioksida (Rentang nilai 0-80)",
        )

        st.markdown('<p style="font-size: 16px; font-weight: normal; margin-bottom: -40px;">SO2 (ppb)</p>', unsafe_allow_html=True)
        so2_input = st.number_input(
            "",
            min_value=0,
            max_value=3000,
            step=1,
            value=None,
            help="Sulfur Dioksida (Rentang nilai 0-380)",
        )

    # Center the calculate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        calculate_button = st.button("Hitung AQI", use_container_width=True)

    if calculate_button:
        if all(
            v is not None
            for v in [pm25_input, pm10_input, co_input, no2_input, o3_input, so2_input]
        ):
            try:
                # Input values to fuzzy system
                aqi_system.input["PM2.5"] = pm25_input
                aqi_system.input["PM10"] = pm10_input
                aqi_system.input["CO"] = co_input
                aqi_system.input["NO2"] = no2_input
                aqi_system.input["O3"] = o3_input
                aqi_system.input["SO2"] = so2_input

                # Calculate AQI
                aqi_system.compute()
                aqi_value = float(aqi_system.output["AQI"])

                # Get category and color
                color, category = get_category_color(aqi_value)

                # Display gauge chart
                st.plotly_chart(
                    create_gauge_chart(aqi_value, "Indeks Kualitas Udara (AQI)"),
                    use_container_width=True,
                )

                # Display results with styling
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 10px 10px; background-color: {color}; border-radius: 10px;'>
                        <h4 style='margin: 0;'>Kategori: {category}</h4>
                        <h4 style='margin: 10px 0;'>AQI: {aqi_value:.1f}</h4>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                # Show recommendations based on category
                st.markdown('<h4 style="margin-top: 20px;">Rekomendasi</h4>', unsafe_allow_html=True)
                if category == "Baik":
                    st.success(
                        "✅ Kualitas udara memuaskan dan polusi udara menimbulkan risiko kecil atau tidak ada risiko."
                    )
                elif category == "Sedang":
                    st.info(
                        "ℹ️ Kualitas udara dapat diterima, namun bagi sebagian kecil orang yang sangat sensitif mungkin perlu berhati-hati."
                    )
                elif category == "Buruk":
                    st.warning(
                        "⚠️ Anggota kelompok sensitif mungkin mengalami dampak kesehatan. Masyarakat umum cenderung tidak terpengaruh."
                    )
                elif category == "Tidak Sehat":
                    st.error(
                        "🚫 Setiap orang mungkin mulai mengalami dampak kesehatan. Kelompok sensitif mungkin mengalami dampak lebih serius."
                    )
                elif category == "Parah":
                    st.error(
                        "⚠️ Peringatan kesehatan: setiap orang dapat mengalami dampak kesehatan yang lebih serius."
                    )
                else:  # Berbahaya
                    st.error(
                        "☠️ Peringatan kesehatan darurat. Seluruh populasi kemungkinan terkena dampak."
                    )

            except Exception as e:
                st.error(f"Terjadi kesalahan dalam perhitungan: {str(e)}")
        else:
            st.error("Mohon isi semua nilai parameter untuk menghitung AQI.")


def main():
    # Add custom CSS
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            margin-top: 16px;
            padding: 10px 20px;
            font-size: 20px;
        }
        .stButton>button:hover {
            background-color: #1976D2;
            color: white;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar navigation
    page = st.sidebar.selectbox("Pilih Halaman", ["Informasi AQI", "Kalkulator AQI"])

    if page == "Kalkulator AQI":
        show_calculator_page()
    else:
        show_info_page()
    
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

if __name__ == "__main__":
    main()

