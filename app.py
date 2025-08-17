import streamlit as st
from recm import recommend, df  # fixed import

st.set_page_config(page_title="AutoMatch – Find Your Perfect Car", layout="wide")

# App title (centered)
st.markdown(
    "<h1 style='text-align: center;'>🚗 AutoMatch – Find Your Perfect Car</h1>",
    unsafe_allow_html=True,
)

# Dropdown search bar
car_name = st.selectbox("🔍 Search for a car", df["CarName"].unique())

if car_name:
    results = recommend(car_name, top_n=4)  # exactly 4 cars
    if not results.empty:
        selected_car = df[df["CarName"] == car_name].iloc[0]

        # Car details header (centered)
        st.markdown(
            f"<h3 style='text-align: center;'>📌 Details of {car_name}</h3>",
            unsafe_allow_html=True,
        )

        # Car details in one line
        st.markdown(
            f"<p style='text-align: center;'>"
            f"• Price: ₹ {selected_car['Price (₹ Lakh)']:.2f} Lakh "
            f"• Engine: {int(selected_car['Engine_L']*1000)} cc "
            f"• Power: {selected_car['Horsepower']:.1f} HP "
            f"• Torque: {int(selected_car['Torque_Nm'])} Nm "
            f"• 0–100 km/h: {selected_car['ZeroTo100']:.1f} sec"
            f"</p>",
            unsafe_allow_html=True,
        )

        # Recommendations header (centered)
        st.markdown(
            "<h3 style='text-align: center;'>🤝 Recommended Cars for You</h3>",
            unsafe_allow_html=True,
        )

        # Show recommendations
        for _, row in results.iterrows():
            st.markdown(
                f"<p style='text-align: center;'>"
                f"<b>{row['CarName']}</b><br>"
                f"• Price: ₹ {row['Price (₹ Lakh)']:.2f} Lakh "
                f"• Engine: {int(row['Engine_L']*1000)} cc "
                f"• Power: {row['Horsepower']:.1f} HP "
                f"• Torque: {int(row['Torque_Nm'])} Nm"
                f"</p><br>",
                unsafe_allow_html=True,
            )
    else:
        st.warning("No recommendations found for this car.")
