# app.py
import streamlit as st
import pandas as pd
from recm import recommend

# Helper function to format price in Lakh / Crore
def format_price(price_lakh: float) -> str:
    if price_lakh >= 100:
        return f"₹ {price_lakh/100:.2f} Crore"
    else:
        return f"₹ {price_lakh:.2f} Lakh"

# Load dataset
df = pd.read_csv("cars_cleaned.csv")

# Convert units
df["Price (₹ Lakh)"] = (df["Price_USD"] * 87) / 100000
df["Engine (cc)"] = df["Engine_L"] * 1000
df["Torque (Nm)"] = df["Torque_lbft"] * 1.35582
df["0-100 km/h (s)"] = df["ZeroTo60"] * 1.60934 / 0.44704
df["CarName"] = df["Make"] + " " + df["Model"]

# Streamlit UI setup
st.set_page_config(page_title="AutoMatch", layout="wide")
st.title("🚗 AutoMatch – Find Your Perfect Car")

# Car selection
car_list = df["CarName"].unique()
selected_car = st.selectbox("🔍 Search for a car", [""] + sorted(car_list))

if selected_car:
    car_data = df[df["CarName"] == selected_car].iloc[0]

    st.subheader(f"📌 Details of {selected_car}")
    st.write(
        f"""
        • Price: {format_price(car_data['Price (₹ Lakh)'])}\n
        • Engine: {car_data['Engine (cc)']:.0f} cc\n
        • Power: {car_data['Horsepower']} HP\n
        • Torque: {car_data['Torque (Nm)']:.0f} Nm\n
        • 0–100 km/h: {car_data['0-100 km/h (s)']:.1f} sec\n
        """
    )

    st.subheader("🤝 Recommended Cars for You")
    recs = recommend(selected_car, top_n=4)

    if not recs.empty:
        cols = st.columns(len(recs))
        for col, (_, row) in zip(cols, recs.iterrows()):
            with col:
                st.markdown(f"### {row['Make']} {row['Model']}")
                st.write(
                    f"""
                    • Price: {format_price(row['Price_USD']*87/100000)}\n
                    • Engine: {row['Engine_L']*1000:.0f} cc\n
                    • Power: {row['Horsepower']} HP\n
                    • Torque: {row['Torque_lbft']*1.35582:.0f} Nm\n
                    """
                )
    else:
        st.info("No similar cars found.")
