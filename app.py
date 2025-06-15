import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

st.set_page_config(page_title="Geneva Climate Dashboard", layout="centered")

st.title("🌍 Geneva Climate Change Explorer")
st.markdown("Data source: [Météo Genève (1962–Present)](https://statistique.ge.ch/domaines/02/02_02/tableaux.asp#3)")

# Connect to SQLite DB
conn = sqlite3.connect("geneva_weather.db")

# Load full data from DB
df = pd.read_sql("SELECT * FROM weather", conn)

# Create Tabs with spacing
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Trends", "📌 Highlights", "📈 Power BI Report"])

# ======================
# TAB 1: TRENDS
# ======================
with tab1:
    # Year Range Filter
    st.subheader("📈 Explore Trends Over Time")
    year_range = st.slider(
        "Select Year Range",
        int(df["Year"].min()),
        int(df["Year"].max()),
        (1990, 2024)
    )

    filtered_query = f"""
        SELECT * FROM weather
        WHERE Year BETWEEN {year_range[0]} AND {year_range[1]}
    """
    filtered_df = pd.read_sql(filtered_query, conn)

    # Temperature
    st.subheader("🌡️ Average Temperature Over Time")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(filtered_df['Year'], filtered_df['Avg Temp (°C)'], marker='o', color='orangered', linewidth=2)
    avg_temp = filtered_df['Avg Temp (°C)'].mean()
    ax1.axhline(avg_temp, color='gray', linestyle='--', label=f"Mean: {avg_temp:.2f}°C")
    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel("Temperature (°C)", fontsize=12)
    ax1.set_title("Average Annual Temperature", fontsize=16)
    ax1.set_xticks(np.arange(filtered_df['Year'].min(), filtered_df['Year'].max() + 1, 5))
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend()
    plt.tight_layout()
    st.pyplot(fig1)

    # Rainfall
    st.subheader("☔ Total Rainfall per Year")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.bar(filtered_df['Year'], filtered_df['Total Rain (mm)'], color='royalblue')
    avg_rain = filtered_df['Total Rain (mm)'].mean()
    ax2.axhline(avg_rain, color='gray', linestyle='--', label=f"Mean: {avg_rain:.0f} mm")
    ax2.set_xlabel("Year", fontsize=12)
    ax2.set_ylabel("Rainfall (mm)", fontsize=12)
    ax2.set_title("Total Rainfall per Year", fontsize=16)
    ax2.set_xticks(np.arange(filtered_df['Year'].min(), filtered_df['Year'].max() + 1, 5))
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend()
    plt.tight_layout()
    st.pyplot(fig2)

    # Sunshine
    st.subheader("☀️ Sunshine Hours per Year")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(filtered_df['Year'], filtered_df['Sunshine Hours'], color='seagreen', marker='o', linewidth=2)
    avg_sun = filtered_df['Sunshine Hours'].mean()
    ax3.axhline(avg_sun, color='gray', linestyle='--', label=f"Mean: {avg_sun:.0f} hrs")
    ax3.set_xlabel("Year", fontsize=12)
    ax3.set_ylabel("Hours", fontsize=12)
    ax3.set_title("Sunshine Hours per Year", fontsize=16)
    ax3.set_xticks(np.arange(filtered_df['Year'].min(), filtered_df['Year'].max() + 1, 5))
    ax3.grid(True, linestyle='--', alpha=0.5)
    ax3.legend()
    plt.tight_layout()
    st.pyplot(fig3)

    # Snow
    st.subheader("❄️ Snowfall per Year")
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.bar(filtered_df['Year'], filtered_df['Snow (cm)'], color='slategray')
    avg_snow = filtered_df['Snow (cm)'].mean()
    ax4.axhline(avg_snow, color='gray', linestyle='--', label=f"Mean: {avg_snow:.0f} cm")
    ax4.set_xlabel("Year", fontsize=12)
    ax4.set_ylabel("Snowfall (cm)", fontsize=12)
    ax4.set_title("Total Snowfall per Year", fontsize=16)
    ax4.set_xticks(np.arange(filtered_df['Year'].min(), filtered_df['Year'].max() + 1, 5))
    ax4.grid(True, linestyle='--', alpha=0.5)
    ax4.legend()
    plt.tight_layout()
    st.pyplot(fig4)

# ======================
# TAB 2: HIGHLIGHTS
# ======================
with tab2:
    st.subheader("📊 Yearly Extremes Dashboard")

    hottest = df.loc[df["Avg Temp (°C)"].idxmax()]
    coldest = df.loc[df["Avg Temp (°C)"].idxmin()]
    wettest = df.loc[df["Total Rain (mm)"].idxmax()]
    driest = df.loc[df["Total Rain (mm)"].idxmin()]
    snowiest = df.loc[df["Snow (cm)"].idxmax()]
    least_snow = df.loc[df["Snow (cm)"].idxmin()]
    sunniest = df.loc[df["Sunshine Hours"].idxmax()]
    darkest = df.loc[df["Sunshine Hours"].idxmin()]
    hottest_day = df.loc[df["Max Temp"].idxmax()]
    coldest_day = df.loc[df["Min Temp"].idxmin()]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔥 Hottest Year (Avg)", f"{int(hottest['Year'])}", f"{hottest['Avg Temp (°C)']:.2f}°C")
        st.write("")
        st.metric("🌡️ Max Temp Ever", f"{int(hottest_day['Year'])}", f"{hottest_day['Max Temp']:.1f}°C")
        st.write("")
        st.metric("☔ Wettest Year", f"{int(wettest['Year'])}", f"{wettest['Total Rain (mm)']:.0f} mm")
        st.write("")
        st.metric("❄️ Snowiest Year", f"{int(snowiest['Year'])}", f"{snowiest['Snow (cm)']:.0f} cm")
        st.write("")
        st.metric("☀️ Sunniest Year", f"{int(sunniest['Year'])}", f"{sunniest['Sunshine Hours']:.0f} hrs")

    with col2:
        st.metric("❄️ Coldest Year (Avg)", f"{int(coldest['Year'])}", f"{coldest['Avg Temp (°C)']:.2f}°C")
        st.write("")
        st.metric("🧊 Min Temp Ever", f"{int(coldest_day['Year'])}", f"{coldest_day['Min Temp']:.1f}°C")
        st.write("")
        st.metric("💧 Driest Year", f"{int(driest['Year'])}", f"{driest['Total Rain (mm)']:.0f} mm")
        st.write("")
        st.metric("❄️ Least Snow", f"{int(least_snow['Year'])}", f"{least_snow['Snow (cm)']:.0f} cm")
        st.write("")
        st.metric("🌑 Least Sunny Year", f"{int(darkest['Year'])}", f"{darkest['Sunshine Hours']:.0f} hrs")

# ======================
# TAB 3: POWER BI REPORT
# ======================
with tab3:
    st.subheader("📊 Interactive Power BI Dashboard")
    st.markdown("This interactive report is hosted on Power BI Service and embedded here.")
    with open("Geneva Weather since 1962.pdf", "rb") as f:
        st.download_button(
            label="📄 Click here to download the PDF version",
            data=f,
            file_name="Geneva Weather since 1962.pdf",
            mime="application/pdf"
        )
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=2217ab57-c747-4d04-9103-9cdc68d2a388&autoAuth=true&ctid=a657607d-9ab9-47c7-8df4-3fd4e6c3294b&actionBarEnabled=true"
    st.components.v1.iframe(src=powerbi_url, height=800, width=1100)
