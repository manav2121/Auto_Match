import streamlit as st
import pandas as pd
from recm import recommend, df  # importing function + dataframe

st.set_page_config(page_title="🚗 AutoMatch", layout="wide")

# App title
st.markdown(
    "<h1 style='text-align: center;'>🚗 AutoMatch – Find Your Perfect Car</h1>",
    unsafe_allow_html=True,
)

# Car selection with placeholder
car_list = df["CarName"].tolist()
car_options = ["-- Select a Car --"] + car_list
selected_car = st.selectbox("🔍 Search for a car", car_options)

# Only show details if user selects a real car
if selected_car != "-- Select a Car --":
    # Spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Show selected car details
    car_details = df[df["CarName"] == selected_car].iloc[0]

    st.markdown(
        "<h3 style='text-align: center;'>📌 Details of {selected_car}</h3>",
        unsafe_allow_html=True,
    )
         
     <br>

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Price", f"₹ {car_details['Price (₹ Lakh)']:.2f} Lakh")
    col2.metric("Engine", f"{car_details['Engine_L']*1000:.0f} cc")
    col3.metric("Power", f"{car_details['Horsepower']:.1f} HP")
    col4.metric("Torque", f"{car_details['Torque_Nm']:.0f} Nm")
    col5.metric("0–100 km/h", f"{car_details['ZeroTo100']:.1f} s")

    # Spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Get recommendations (only 4 cars)
    st.markdown(
        "<h3 style='text-align: center;'>🤝 Recommended Cars for You</h3>",
        unsafe_allow_html=True,
    )
    recommendations = recommend(selected_car, top_n=4)

    if recommendations.empty:
        st.warning("No recommendations found within the price range.")
    else:
        cols = st.columns(2)
        for idx, row in recommendations.iterrows():
            with cols[idx % 2]:
                st.markdown(
                    f"""
                    ### {row['CarName']}
                    • **Price:** ₹ {row['Price (₹ Lakh)']:.2f} Lakh  
                    • **Engine:** {row['Engine_L']*1000:.0f} cc  
                    • **Power:** {row['Horsepower']:.1f} HP  
                    • **Torque:** {row['Torque_Nm']:.0f} Nm  
                    """
                )

