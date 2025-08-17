# recm.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("cars_cleaned.csv")

# Create unique identifier column for cars
df["CarName"] = df["Make"] + " " + df["Model"]

# Convert units for consistency
df["Price (₹ Lakh)"] = (df["Price_USD"] * 87) / 100000
df["Torque_Nm"] = df["Torque_lbft"] * 1.35582
df["ZeroTo100"] = df["ZeroTo60"] * 1.60934 / 0.44704

# Encode categorical features
categorical_cols = ["Make", "Model"]
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(df[categorical_cols]).toarray()

# Combine with numeric features
numeric_features = df[["Year", "Engine_L", "Horsepower", "Torque_Nm", "ZeroTo100", "Price (₹ Lakh)"]].values
feature_matrix = np.hstack([numeric_features, encoded_features])

# Precompute cosine similarity matrix
similarity = cosine_similarity(feature_matrix)

def recommend(car_name, top_n=5, price_tolerance=0.20):
    """
    Recommend cars similar to the selected car,
    prioritizing close prices (±price_tolerance fraction),
    then by cosine similarity excluding the same brand.

    Args:
        car_name: full car name (Make + Model)
        top_n: number of recommendations
        price_tolerance: fraction of price range for filtering (default ±20%)

    Returns:
        DataFrame with recommended cars.
    """
    if car_name not in df["CarName"].values:
        return pd.DataFrame()

    idx = df.index[df["CarName"] == car_name][0]
    selected_car = df.iloc[idx]
    selected_price = selected_car["Price (₹ Lakh)"]

    # Define price range filter ±20%
    lower_price = selected_price * (1 - price_tolerance)
    upper_price = selected_price * (1 + price_tolerance)

    # Filter indices of cars within price range, excluding the selected car itself
    price_filtered_indices = df[
        (df["Price (₹ Lakh)"] >= lower_price) &
        (df["Price (₹ Lakh)"] <= upper_price) &
        (df.index != idx)
    ].index.tolist()

    if not price_filtered_indices:
        # fallback: no cars in price range, return empty dataframe
        return pd.DataFrame()

    # Compute similarity scores only for filtered cars
    sim_scores = [(i, similarity[idx][i]) for i in price_filtered_indices]

    # Sort by similarity descending
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Exclude same brand as selected car
    selected_brand = selected_car["Make"]
    filtered_scores = [(i, score) for i, score in sim_scores if df.iloc[i]["Make"] != selected_brand]

    # Ensure unique brands
    seen_brands = set()
    unique_indices = []
    for i, _ in filtered_scores:
        brand = df.iloc[i]["Make"]
        if brand not in seen_brands:
            seen_brands.add(brand)
            unique_indices.append(i)
        if len(unique_indices) >= top_n:
            break

    return df.iloc[unique_indices].reset_index(drop=True)

