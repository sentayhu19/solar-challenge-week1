import streamlit as st
import pandas as pd
from utils import (
    load_data,
    create_metric_boxplot,
    calculate_summary_stats,
    create_ghi_ranking,
    create_correlation_heatmap
)

st.set_page_config(
    page_title="Solar Potential Analysis",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main {background-color: #f5f5f5}
        .stButton>button {background-color: #4CAF50; color: white;}
        .stSelectbox {min-width: 200px;}
    </style>
""", unsafe_allow_html=True)

st.title("☀️ Cross-Country Solar Potential Analysis")
st.markdown("""Analyze and compare solar potential across different countries using key metrics:  
- **GHI**: Global Horizontal Irradiance  
- **DNI**: Direct Normal Irradiance  
- **DHI**: Diffuse Horizontal Irradiance""")

file_paths = {
    'Benin': '../data/benin_clean.csv',
    'Sierra Leone': '../data/sierraleone_clean.csv',
    'Togo': '../data/togo_clean.csv'
}

try:
    # Load data
    data = load_data(file_paths)
    metrics = ['GHI', 'DNI', 'DHI']

    # Sidebar controls
    st.sidebar.header("📊 Visualization Options")
    
    # Metric selection with help
    selected_metric = st.sidebar.selectbox(
        "Select Metric for Analysis",
        metrics,
        help="Choose which solar radiation metric to analyze"
    )

    # Country selection
    selected_countries = st.sidebar.multiselect(
        "Select Countries to Compare",
        data['Country'].unique(),
        default=data['Country'].unique(),
        help="Choose which countries to include in the analysis"
    )

    filtered_data = data[data['Country'].isin(selected_countries)]

    if 'Date' in filtered_data.columns:
        st.sidebar.date_input(
            "Select Date Range",
            value=(filtered_data['Date'].min(), filtered_data['Date'].max()),
            help="Filter data by date range"
        )

    st.sidebar.download_button(
        label="📥 Download Data",
        data=filtered_data.to_csv(index=False),
        file_name="solar_data.csv",
        mime="text/csv"
    )

    tab1, tab2, tab3 = st.tabs(["📈 Distribution Analysis", "📊 Rankings", "🔍 Detailed Statistics"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{selected_metric} Distribution by Country")
            fig = create_metric_boxplot(filtered_data, selected_metric)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Correlation Heatmap")
            fig = create_correlation_heatmap(filtered_data, metrics)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Solar Potential Rankings")
        fig = create_ghi_ranking(filtered_data)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Summary Statistics")
        stats_df = calculate_summary_stats(filtered_data, metrics)
        st.dataframe(
            stats_df.style.highlight_max(axis=0, color='lightgreen'),
            use_container_width=True
        )

        if len(selected_countries) > 1:
            st.subheader("Statistical Significance")
            from scipy import stats
            f_stat, p_value = stats.f_oneway(
                *[group[selected_metric].values for name, group in filtered_data.groupby('Country')]
            )
            st.write(f"One-way ANOVA p-value for {selected_metric}: {p_value:.4f}")

except FileNotFoundError:
    st.error("⚠️ Data files not found. Please ensure all required CSV files are present in the data directory.")
    st.info("📁 Expected files: benin_clean.csv, sierraleone_clean.csv, togo_clean.csv")
