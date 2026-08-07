import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

# --- 1. GENERATE BANGALORE DEMAND DATA ---
@st.cache_data
def generate_demand_data(num_orders=3000):
    np.random.seed(42) # Ensure the map looks the same every time
    
    # Coordinates for major tech/student hubs in Bangalore
    hubs = {
        "Koramangala": [12.9279, 77.6271],
        "Whitefield": [12.9698, 77.7499],
        "HSR Layout": [12.9121, 77.6446],
        "Indiranagar": [12.9784, 77.6408],
        "Electronic City": [12.8452, 77.6602]
    }
    
    data = []
    # Generate random orders clustered around these hubs
    for hub, coords in hubs.items():
        # Create 600 orders per hub with slight geographical spread (variance)
        latitudes = np.random.normal(coords[0], 0.015, int(num_orders/len(hubs)))
        longitudes = np.random.normal(coords[1], 0.015, int(num_orders/len(hubs)))
        
        for lat, lon in zip(latitudes, longitudes):
            data.append([lat, lon, hub])
            
    df = pd.DataFrame(data, columns=['Latitude', 'Longitude', 'Zone'])
    return df

# --- 2. TRAIN CUSTOM K-MEANS MODEL ---
def optimize_store_locations(df, num_stores):
    # Extract just the coordinates for the machine learning model
    coordinates = df[['Latitude', 'Longitude']]
    
    # Initialize and train the K-Means clustering algorithm
    kmeans = KMeans(n_clusters=num_stores, random_state=42, n_init=10)
    df['Assigned_Store'] = kmeans.fit_predict(coordinates)
    
    # The 'cluster_centers_' represent the mathematically optimal Dark Store GPS locations
    store_locations = pd.DataFrame(kmeans.cluster_centers_, columns=['Latitude', 'Longitude'])
    store_locations['Store_ID'] = [f"DS-{i+1}" for i in range(num_stores)]
    
    return df, store_locations

# --- 3. STREAMLIT UI & DASHBOARD ---
st.set_page_config(page_title="Flipkart Minutes: Dark Store Optimization", layout="wide")

st.title("⚡ Flipkart Minutes: Dark Store Network Optimization")
st.markdown("Facility location model using K-Means clustering to minimize last-mile delivery TAT.")

# Load the customer demand data
demand_df = generate_demand_data()

# Sidebar Controls
st.sidebar.header("Network Constraints")
st.sidebar.markdown("Adjust the capital expenditure budget by increasing or decreasing the number of active dark stores.")
num_stores = st.sidebar.slider("Number of Dark Stores to Open", min_value=2, max_value=10, value=5)

# Run the custom clustering model
assigned_demand, optimal_stores = optimize_store_locations(demand_df, num_stores)

# --- 4. RENDER THE INTERACTIVE MAP ---
# Center the map on Bangalore
m = folium.Map(location=[12.9716, 77.5946], zoom_start=11, tiles="CartoDB positron")

# Plot a sample of customer orders (Plotting all 3000 slows down the browser)
sample_demand = assigned_demand.sample(500, random_state=42)
for _, row in sample_demand.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=2,
        color="red",
        fill=True,
        fill_opacity=0.4
    ).add_to(m)

# Plot the optimal Dark Store locations determined by the ML model
for _, row in optimal_stores.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"<b>{row['Store_ID']}</b><br>Optimized Node",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(m)

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Customer Orders Analyzed", len(demand_df))
col2.metric("Active Dark Stores", num_stores)
col3.metric("Avg. Orders per Store", int(len(demand_df) / num_stores))

st.divider()

# Display Map in Streamlit
st_folium(m, width=1200, height=600)

# Display the exact coordinates for operations teams
st.subheader("📍 Deployment Output: Optimal GPS Coordinates")
st.dataframe(optimal_stores[['Store_ID', 'Latitude', 'Longitude']], use_container_width=True)