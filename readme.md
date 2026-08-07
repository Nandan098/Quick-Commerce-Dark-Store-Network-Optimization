#  Quick Commerce Dark Store Network Optimization

A spatial facility location model and interactive dashboard built with **Python**, **Scikit-Learn (K-Means)**, **Folium**, and **Streamlit**. Designed to optimize micro-fulfillment center (Dark Store) placements for 10-minute quick commerce delivery networks like Flipkart Minutes.

---

##  Overview & Business Context

In the hyper-competitive quick commerce (Q-Commerce) space, delivering groceries and essentials within 10 to 15 minutes is the standard SLA. Traditional massive Fulfillment Centers (FCs) located on the outskirts of a city cannot meet these timelines. Instead, companies must lease expensive, smaller real estate (Dark Stores) deep inside high-density urban neighborhoods.

The business challenge is **Capital Expenditure (CapEx) vs. SLA Coverage**: 
* *How do we maximize the number of customers within a 2-kilometer radius while opening the fewest possible dark stores?*

This project solves this by replacing guesswork with mathematical clustering. It simulates localized customer demand across a major tech hub (Bangalore) and uses Machine Learning to calculate the exact geographical coordinates where dark stores should be established to minimize Last-Mile Turnaround Time (TAT).

---

## Key Features

* **Custom Demand Simulation:** Automatically generates a realistic mock dataset of 3,000+ customer GPS drops clustered around heavy-volume tech and student hubs (e.g., Koramangala, HSR Layout, Whitefield).
* **Machine Learning Facility Allocation:** Utilizes a custom `Scikit-Learn` K-Means clustering algorithm to mathematically determine the optimal center of gravity (centroids) for customer demand zones.
* **Dynamic Geolocation Mapping:** Integrates `Folium` to render an interactive street-level map, allowing operations teams to visually track proposed dark store nodes and customer assignment radii.
* **CapEx Scenario Planning:** Features an interactive Streamlit slider to adjust network constraints (number of active stores). The ML model recalculates optimal real estate locations in real-time as the budget shifts.

---

## Technical Architecture & Stack

* **Language:** Python 3.9+
* **Machine Learning:** Scikit-Learn (K-Means Clustering)
* **Data Processing:** Pandas, NumPy
* **Mapping & GIS:** Folium, Streamlit-Folium
* **Frontend Dashboard:** Streamlit

---

