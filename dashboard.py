import streamlit as st
import pandas as pd
import numpy as np
from agents import ForecastingAgent, StoreAgent, WarehouseAgent, SupplierAgent, CustomerAgent, PricingAgent

# Load Data
demand_data = pd.read_csv("data/demand_forecasting.csv")
store_data = pd.read_csv("data/inventory_monitoring.csv")
warehouse_data = pd.read_csv("data/inventory_monitoring.csv")  # Using same for now

# Forecast Demand
forecasting_agent = ForecastingAgent(demand_data)
predicted_demand = forecasting_agent.predict_demand()

# Check Restock Needs
store_agent = StoreAgent(store_data, predicted_demand)
restock_list = store_agent.check_restock_needed()

# Warehouse Fulfillment
warehouse_agent = WarehouseAgent(warehouse_data)
fulfillment_results = warehouse_agent.fulfill_requests(restock_list)

# Supplier Replenishment
supplier_agent = SupplierAgent()
restocked_items = supplier_agent.restock_warehouse(warehouse_agent)

# Simulated Customer Purchases (NEW)
def simulate_customer_purchases(store_data):
    modified_data = store_data.copy()
    modified_data['Simulated Purchases'] = np.random.randint(5, 50, size=len(modified_data))
    modified_data['Updated Stock'] = modified_data['Stock Levels'] - modified_data['Simulated Purchases']
    modified_data['Updated Stock'] = modified_data['Updated Stock'].apply(lambda x: x if x > 0 else 0)
    return modified_data[['Store ID', 'Product ID', 'Stock Levels', 'Simulated Purchases', 'Updated Stock']]

simulated_customer_data = simulate_customer_purchases(store_data)

# Streamlit Dashboard
st.set_page_config(layout="wide", page_title="Multi-Agent Inventory Dashboard", page_icon="📦")
st.title("📦 Multi-Agent Inventory Management System")
st.markdown("""
<style>
    .main {background-color: #f7f9fa;}
    .block-container {padding-top: 2rem;}
    h1, h2, h3 {color: #333333;}
    .stMetric {background: #000; border: 1px solid #ddd; border-radius: 10px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

# --- Overview Section ---
st.header("📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("🛍️ Unique Products", demand_data['Product ID'].nunique())
col2.metric("🏪 Total Stores", store_data['Store ID'].nunique())
col3.metric("📈 Forecast Records", len(predicted_demand))

# --- Demand Forecast Section ---
st.header("📈 Demand Forecast")
st.dataframe(predicted_demand, use_container_width=True)
product_filter = st.text_input("🔍 Filter by Product ID:", "")
if product_filter:
    filtered = predicted_demand[predicted_demand['Product ID'].astype(str).str.contains(product_filter)]
    st.dataframe(filtered, use_container_width=True)

# --- Restock Recommendations Section ---
st.header("🛒 Smart Restock Recommendations")
if restock_list:
    restock_df = pd.DataFrame(restock_list)
    st.dataframe(restock_df, use_container_width=True)
else:
    st.info("All stores are sufficiently stocked based on predicted demand.")

# --- Warehouse Fulfillment Section ---
st.header("🏬 Warehouse Fulfillment Status")
if fulfillment_results:
    fulfillment_df = pd.DataFrame(fulfillment_results)
    st.dataframe(fulfillment_df, use_container_width=True)
    status_counts = fulfillment_df['Status'].value_counts()
    st.write("### ✅ Fulfillment Summary")
    st.bar_chart(status_counts)
else:
    st.info("No fulfillment actions were taken.")

# --- Supplier Restocking Section ---
st.header("🚛 Supplier Restocking Summary")
if restocked_items:
    restocked_df = pd.DataFrame(restocked_items)
    st.dataframe(restocked_df, use_container_width=True)
    st.write("### 🔄 Restocking Actions Summary")
    st.bar_chart(restocked_df['Restocked By'].value_counts())
else:
    st.info("No restocking was needed from the supplier.")

# --- Inventory Health Overview ---
st.header("📦 Inventory Health Overview")
store_options = store_data['Store ID'].unique()
selected_store = st.selectbox("🏪 Select a Store ID to Inspect:", store_options)

store_view = store_data[store_data['Store ID'] == selected_store].copy()
merged = store_view.merge(predicted_demand, on="Product ID", how="left")
merged['Shortage'] = merged['Predicted Demand'] - merged['Stock Levels']
merged['Shortage'] = merged['Shortage'].apply(lambda x: x if x > 0 else 0)

st.dataframe(merged[['Product ID', 'Stock Levels', 'Predicted Demand', 'Shortage']], use_container_width=True)

st.write("### 🔍 Stock vs Demand for Selected Store")
st.bar_chart(merged.set_index("Product ID")[['Stock Levels', 'Predicted Demand']])

# --- Customer Simulation Section ---
st.header("🧑‍💼 Customer Simulation")
customer_agent = CustomerAgent()
st.markdown(f"**{customer_agent.name} Role:** {customer_agent.role()}")
st.dataframe(simulated_customer_data, use_container_width=True)

# --- Pricing Analysis Section ---
st.header("💰 Pricing Strategy Insights")
pricing_agent = PricingAgent()
st.markdown(f"**{pricing_agent.name}**")
st.dataframe(pricing_agent.data.head(), use_container_width=True)

st.success("✅ All key multi-agent system insights now available in your dashboard, including customer simulation.")
