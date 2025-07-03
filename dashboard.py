
# import streamlit as st
# import pandas as pd
# import numpy as np
# import altair as alt
# from agents import ForecastingAgent, StoreAgent, WarehouseAgent, SupplierAgent, CustomerAgent, PricingAgent

# # Load Data
# demand_data = pd.read_csv("data/demand_forecasting.csv")
# store_data = pd.read_csv("data/inventory_monitoring.csv")
# warehouse_data = pd.read_csv("data/inventory_monitoring.csv")

# # Agents and Results
# forecasting_agent = ForecastingAgent(demand_data)
# predicted_demand = forecasting_agent.predict_demand()

# store_agent = StoreAgent(store_data, predicted_demand)
# restock_list = store_agent.check_restock_needed()

# warehouse_agent = WarehouseAgent(warehouse_data)
# fulfillment_results = warehouse_agent.fulfill_requests(restock_list)

# supplier_agent = SupplierAgent()
# restocked_items = supplier_agent.restock_warehouse(warehouse_agent)

# # Customer Simulation
# def simulate_customer_purchases(store_data):
#     modified_data = store_data.copy()
#     modified_data['Simulated Purchases'] = np.random.randint(5, 50, size=len(modified_data))
#     modified_data['Updated Stock'] = modified_data['Stock Levels'] - modified_data['Simulated Purchases']
#     modified_data['Updated Stock'] = modified_data['Updated Stock'].apply(lambda x: x if x > 0 else 0)
#     return modified_data[['Store ID', 'Product ID', 'Stock Levels', 'Simulated Purchases', 'Updated Stock']]

# simulated_customer_data = simulate_customer_purchases(store_data)

# # Streamlit Page Config
# st.set_page_config(layout="wide", page_title="Multi-Agent Inventory Dashboard", page_icon="📦")

# st.markdown("""
#     <style>
#         section[data-testid="stSidebar"] {
#             min-width: 320px !important;
#             max-width: 320px !important;
#             width: 320px !important;
#         }
#         thead tr th {
#             position: sticky;
#             top: 0;
#             background-color: white;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar Navigation
# st.sidebar.title("📋 Dashboard Navigation")
# section = st.sidebar.radio(
#     "Go to section:",
#     [
#         "📈 Overview",
#         "📈 Demand Forecast",
#         "🍎 Restock Recommendations",
#         "🏬 Warehouse Fulfillment",
#         "🚛 Supplier Restocking",
#         "📦 Inventory Health",
#         "🧑‍💼 Customer Simulation",
#         "💰 Pricing Insights"
#     ]
# )

# # Main Title
# st.title("📦 Multi-Agent Inventory Management System")

# # Filters
# with st.expander("🔧 Filters"):
#     selected_store = st.selectbox("🏪 Select Store:", ["All"] + list(store_data["Store ID"].unique()))
#     selected_product = st.text_input("🔍 Filter by Product ID")

# # Overview Section
# if section == "📊 Overview":
#     st.header("📊 Dashboard Overview")

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("🛍️ Unique Products", demand_data['Product ID'].nunique())
#     col2.metric("🏪 Total Stores", store_data['Store ID'].nunique())
#     col3.metric("📈 Forecast Records", len(predicted_demand))
#     col4.metric("📦 Restock Actions", len(restock_list))

#     total_demand = predicted_demand['Predicted Demand'].sum()
#     shortages = store_data.merge(predicted_demand, on="Product ID", how="left")
#     shortages['Shortage'] = shortages['Predicted Demand'] - shortages['Stock Levels']
#     low_stock_count = (shortages['Shortage'] > 0).sum()

#     col5, col6 = st.columns(2)
#     col5.metric("📊 Total Predicted Demand", int(total_demand))
#     col6.metric("⚠️ Low Stock Products", low_stock_count)

#     st.subheader("🔥 Top 10 Products by Predicted Demand")
#     top_products = predicted_demand.groupby("Product ID")["Predicted Demand"].sum().sort_values(ascending=False).head(10).reset_index()
#     chart = alt.Chart(top_products).mark_bar(color="#4e79a7").encode(
#         x=alt.X("Product ID:N", sort='-y'),
#         y=alt.Y("Predicted Demand:Q"),
#         tooltip=["Product ID", "Predicted Demand"]
#     ).properties(height=300)
#     st.altair_chart(chart, use_container_width=True)

#     st.subheader("📉 Stock Status Summary")
#     stock_status = pd.DataFrame({
#         "Status": ["Restock Needed", "Sufficient"],
#         "Count": [low_stock_count, len(shortages) - low_stock_count]
#     })
#     pie_chart = alt.Chart(stock_status).mark_arc(innerRadius=50).encode(
#         theta="Count:Q",
#         color="Status:N",
#         tooltip=["Status", "Count"]
#     ).properties(height=300)
#     st.altair_chart(pie_chart, use_container_width=True)

#     if low_stock_count > 20:
#         st.warning("⚠️ High number of low-stock products detected. Consider restocking priority SKUs.")
#     elif low_stock_count == 0:
#         st.success("✅ All products are currently well-stocked!")

#     st.download_button("📥 Download Overview Metrics", stock_status.to_csv(index=False), "overview_summary.csv")


# # Demand Forecast Section
# elif section == "📈 Demand Forecast":
#     st.header("📈 Demand Forecast")
#     df = predicted_demand.copy()
#     if selected_product:
#         df = df[df['Product ID'].astype(str).str.contains(selected_product)]
#     st.dataframe(df, use_container_width=True)
#     st.download_button("⬇️ Download Forecast", df.to_csv(index=False), file_name="forecast.csv")

# # Restock Recommendations
# elif section == "🍎 Restock Recommendations":
#     st.header("🍎 Smart Restock Recommendations")
#     if restock_list:
#         restock_df = pd.DataFrame(restock_list)
#         st.dataframe(restock_df, use_container_width=True)
#         st.download_button("⬇️ Download Restock List", restock_df.to_csv(index=False), file_name="restock_list.csv")
#     else:
#         st.info("✅ All stores are sufficiently stocked based on predicted demand.")

# # Warehouse Fulfillment
# elif section == "🏬 Warehouse Fulfillment":
#     st.header("🏬 Warehouse Fulfillment Status")
#     if fulfillment_results:
#         df = pd.DataFrame(fulfillment_results)
#         st.dataframe(df, use_container_width=True)
#         with st.expander("🔍 Fulfillment Summary"):
#             st.bar_chart(df['Status'].value_counts())
#         st.download_button("⬇️ Download Fulfillment Data", df.to_csv(index=False), file_name="fulfillment.csv")
#     else:
#         st.info("📦 No fulfillment actions were taken.")

# # Supplier Restocking
# elif section == "🚛 Supplier Restocking":
#     st.header("🚛 Supplier Restocking Summary")
#     if restocked_items:
#         df = pd.DataFrame(restocked_items)
#         st.dataframe(df, use_container_width=True)
#         with st.expander("🔄 Restocking Summary"):
#             st.bar_chart(df['Restocked By'].value_counts())
#         st.download_button("⬇️ Download Supplier Restock Data", df.to_csv(index=False), file_name="supplier_restock.csv")
#     else:
#         st.info("📭 No restocking was needed from the supplier.")

# # Inventory Health
# elif section == "📦 Inventory Health":
#     st.header("📦 Inventory Health Overview")
#     if selected_store == "All":
#         st.info("Please select a specific store from the filter to inspect inventory.")
#     else:
#         store_view = store_data[store_data['Store ID'] == selected_store].copy()
#         merged = store_view.merge(predicted_demand, on="Product ID", how="left")
#         merged['Shortage'] = merged['Predicted Demand'] - merged['Stock Levels']
#         merged['Shortage'] = merged['Shortage'].apply(lambda x: x if x > 0 else 0)
#         st.dataframe(merged[['Product ID', 'Stock Levels', 'Predicted Demand', 'Shortage']], use_container_width=True)
#         st.write("### 🔍 Stock vs Demand")
#         st.bar_chart(merged.set_index("Product ID")[['Stock Levels', 'Predicted Demand']])

# # Customer Simulation
# elif section == "🧑‍💼 Customer Simulation":
#     st.header("🧑‍💼 Customer Simulation")
#     customer_agent = CustomerAgent()
#     st.markdown(f"**{customer_agent.name} Role:** {customer_agent.role()}")
#     st.dataframe(simulated_customer_data, use_container_width=True)
#     st.download_button("⬇️ Download Simulated Data", simulated_customer_data.to_csv(index=False), file_name="customer_sim.csv")

# # Pricing Insights
# elif section == "💰 Pricing Insights":
#     st.header("💰 Pricing Strategy Insights")
#     pricing_agent = PricingAgent()
#     st.markdown(f"**{pricing_agent.name}**")
#     st.dataframe(pricing_agent.data.head(), use_container_width=True)
#     st.download_button("⬇️ Download Pricing Data", pricing_agent.data.to_csv(index=False), file_name="pricing.csv")

# # Footer
# st.sidebar.markdown("---")
# st.sidebar.success("Navigate through each section to explore the system insights.")

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from agents import ForecastingAgent, StoreAgent, WarehouseAgent, SupplierAgent, CustomerAgent, PricingAgent

# Load Data
demand_data = pd.read_csv("data/demand_forecasting.csv")
store_data = pd.read_csv("data/inventory_monitoring.csv")
warehouse_data = pd.read_csv("data/inventory_monitoring.csv")

# Agents and Results
forecasting_agent = ForecastingAgent(demand_data)
predicted_demand = forecasting_agent.predict_demand()

store_agent = StoreAgent(store_data, predicted_demand)
restock_list = store_agent.check_restock_needed()

warehouse_agent = WarehouseAgent(warehouse_data)
fulfillment_results = warehouse_agent.fulfill_requests(restock_list)

supplier_agent = SupplierAgent()
restocked_items = supplier_agent.restock_warehouse(warehouse_agent)

# Customer Simulation
def simulate_customer_purchases(store_data):
    modified_data = store_data.copy()
    modified_data['Simulated Purchases'] = np.random.randint(5, 50, size=len(modified_data))
    modified_data['Updated Stock'] = modified_data['Stock Levels'] - modified_data['Simulated Purchases']
    modified_data['Updated Stock'] = modified_data['Updated Stock'].apply(lambda x: x if x > 0 else 0)
    return modified_data[['Store ID', 'Product ID', 'Stock Levels', 'Simulated Purchases', 'Updated Stock']]

simulated_customer_data = simulate_customer_purchases(store_data)

# Streamlit Page Config
st.set_page_config(layout="wide", page_title="Multi-Agent Inventory Dashboard", page_icon="📦")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            min-width: 320px !important;
            max-width: 320px !important;
            width: 320px !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 320px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📋 Dashboard Navigation")
section = st.sidebar.radio("Go to section:", [
    "📊 Overview",
    "📈 Demand Forecast",
    "🛒 Restock Recommendations",
    "🏬 Warehouse Fulfillment",
    "🚛 Supplier Restocking",
    "📦 Inventory Health",
    "🧑‍💼 Customer Simulation",
    "💰 Pricing Insights"
])

# Main Title
st.title("📦 Multi-Agent Inventory Management System")

# Overview Section
if section == "📊 Overview":
    st.header("📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛍️ Unique Products", demand_data['Product ID'].nunique())
    col2.metric("🏪 Total Stores", store_data['Store ID'].nunique())
    col3.metric("📈 Forecast Records", len(predicted_demand))
    col4.metric("📦 Restock Actions", len(restock_list))

    total_demand = predicted_demand['Predicted Demand'].sum()
    shortages = store_data.merge(predicted_demand, on="Product ID", how="left")
    shortages['Shortage'] = shortages['Predicted Demand'] - shortages['Stock Levels']
    low_stock_count = (shortages['Shortage'] > 0).sum()

    col5, col6 = st.columns(2)
    col5.metric("📊 Total Predicted Demand", int(total_demand))
    col6.metric("⚠️ Low Stock Products", low_stock_count)

    st.subheader("🔥 Top 10 Products by Predicted Demand")
    top_products = predicted_demand.groupby("Product ID")["Predicted Demand"].sum().sort_values(ascending=False).head(10).reset_index()
    chart = alt.Chart(top_products).mark_bar(color="#4e79a7").encode(
        x=alt.X("Product ID:N", sort='-y'),
        y=alt.Y("Predicted Demand:Q"),
        tooltip=["Product ID", "Predicted Demand"]
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

    st.subheader("📉 Stock Status Summary")
    stock_status = pd.DataFrame({
        "Status": ["Restock Needed", "Sufficient"],
        "Count": [low_stock_count, len(shortages) - low_stock_count]
    })
    pie_chart = alt.Chart(stock_status).mark_arc(innerRadius=50).encode(
        theta="Count:Q",
        color="Status:N",
        tooltip=["Status", "Count"]
    ).properties(height=300)
    st.altair_chart(pie_chart, use_container_width=True)

    if low_stock_count > 20:
        st.warning("⚠️ High number of low-stock products detected. Consider restocking priority SKUs.")
    elif low_stock_count == 0:
        st.success("✅ All products are currently well-stocked!")

    st.download_button("📥 Download Overview Metrics", stock_status.to_csv(index=False), "overview_summary.csv")

# Demand Forecast Section
elif section == "📈 Demand Forecast":
    st.header("📈 Product Demand Forecast")

    product_filter = st.text_input("🔍 Filter by Product ID:")
    df = predicted_demand.copy()

    if product_filter:
        df = df[df['Product ID'].astype(str).str.contains(product_filter)]

    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Demand Distribution")
    hist_chart = alt.Chart(df).mark_bar(color="#f28e2b").encode(
        x=alt.X("Predicted Demand:Q", bin=alt.Bin(maxbins=30)),
        y='count()',
        tooltip=['count()']
    ).properties(height=300)
    st.altair_chart(hist_chart, use_container_width=True)

    st.download_button("📥 Download Forecast Data", df.to_csv(index=False), "predicted_demand.csv")

# Restock Recommendations Section
elif section == "🛒 Restock Recommendations":
    st.header("🛒 Smart Restock Recommendations")

    if restock_list:
        df_restock = pd.DataFrame(restock_list)
        st.dataframe(df_restock, use_container_width=True)

        st.subheader("📌 Restock Summary")
        restock_summary = df_restock['Store ID'].value_counts().reset_index()
        restock_summary.columns = ['Store ID', 'Restock Count']

        bar_chart = alt.Chart(restock_summary).mark_bar(color="#59a14f").encode(
            x=alt.X("Store ID:N", sort='-y'),
            y=alt.Y("Restock Count:Q"),
            tooltip=["Store ID", "Restock Count"]
        ).properties(height=300)
        st.altair_chart(bar_chart, use_container_width=True)

        st.download_button("📥 Download Restock List", df_restock.to_csv(index=False), "restock_recommendations.csv")

    else:
        st.success("✅ All stores are sufficiently stocked based on predicted demand.")

# Warehouse Fulfillment Section
elif section == "🏬 Warehouse Fulfillment":
    st.header("🏬 Warehouse Fulfillment Status")

    if fulfillment_results:
        df_fulfill = pd.DataFrame(fulfillment_results)
        st.dataframe(df_fulfill, use_container_width=True)

        st.subheader("📦 Fulfillment Result Summary")
        summary = df_fulfill['Status'].value_counts().reset_index()
        summary.columns = ['Status', 'Count']

        status_chart = alt.Chart(summary).mark_bar(color="#edc948").encode(
            x=alt.X("Status:N", sort='-y'),
            y=alt.Y("Count:Q"),
            tooltip=["Status", "Count"]
        ).properties(height=300)
        st.altair_chart(status_chart, use_container_width=True)

        st.download_button("📥 Download Fulfillment Data", df_fulfill.to_csv(index=False), "warehouse_fulfillment.csv")

    else:
        st.success("📦 No fulfillment actions were necessary. All demands are currently met.")

# Supplier Restocking Section
elif section == "🚛 Supplier Restocking":
    st.header("🚛 Supplier Restocking Summary")

    if restocked_items:
        df_supplier = pd.DataFrame(restocked_items)
        st.dataframe(df_supplier, use_container_width=True)

        st.subheader("📊 Supplier Actions Breakdown")
        summary = df_supplier['Restocked By'].value_counts().reset_index()
        summary.columns = ['Restocked By', 'Count']

        supplier_chart = alt.Chart(summary).mark_bar(color="#b07aa1").encode(
            x=alt.X("Restocked By:N", sort='-y'),
            y=alt.Y("Count:Q"),
            tooltip=["Restocked By", "Count"]
        ).properties(height=300)
        st.altair_chart(supplier_chart, use_container_width=True)

        st.download_button("📥 Download Supplier Restock Data", df_supplier.to_csv(index=False), "supplier_restock.csv")

    else:
        st.success("🚛 No supplier restocking actions were required at this time.")


# Inventory Health Section
elif section == "📦 Inventory Health":
    st.header("📦 Inventory Health Overview")

    store_options = store_data['Store ID'].unique()
    selected_store = st.selectbox("🏪 Select a Store ID:", store_options)

    store_view = store_data[store_data['Store ID'] == selected_store].copy()
    merged = store_view.merge(predicted_demand, on="Product ID", how="left")
    merged['Shortage'] = merged['Predicted Demand'] - merged['Stock Levels']
    merged['Shortage'] = merged['Shortage'].apply(lambda x: x if x > 0 else 0)

    st.subheader(f"📋 Inventory vs Demand - Store {selected_store}")
    st.dataframe(merged[['Product ID', 'Stock Levels', 'Predicted Demand', 'Shortage']], use_container_width=True)

    st.subheader("📉 Stock vs Predicted Demand Chart")

    # Ensure required columns are present before creating bar chart
    if all(col in merged.columns for col in ['Product ID', 'Stock Levels', 'Predicted Demand']):
        # Prepare chart data
        chart_data = merged[['Store ID', 'Product ID', 'Stock Levels', 'Predicted Demand']].copy()
        chart_data['Simulated Purchases'] = chart_data['Predicted Demand']
        chart_data['Updated Stock'] = chart_data['Stock Levels'] - chart_data['Simulated Purchases']
        chart_data['Updated Stock'] = chart_data['Updated Stock'].apply(lambda x: max(x, 0))

        # Melt chart data into long format
        chart_data = chart_data.melt(
            id_vars=['Store ID', 'Product ID'],
            value_vars=['Stock Levels', 'Simulated Purchases', 'Updated Stock'],
            var_name='Metric',
            value_name='Value'
        )

        # Create the bar chart
        bar_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Product ID:N', title='Product ID'),
            y=alt.Y('Value:Q', title='Units'),
            color=alt.Color('Metric:N', title='Metric'),
            tooltip=[
                alt.Tooltip('Store ID:N'),
                alt.Tooltip('Product ID:N'),
                alt.Tooltip('Metric:N'),
                alt.Tooltip('Value:Q')
            ]
        ).properties(
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.error("Required fields missing for chart generation.")

    # Low stock notification
    low_stock = (merged['Shortage'] > 0).sum()
    if low_stock > 0:
        st.warning(f"⚠️ {low_stock} products in Store {selected_store} are understocked.")
    else:
        st.success(f"✅ All products in Store {selected_store} are sufficiently stocked.")

    # Download report
    st.download_button(
        label="📥 Download Store Health Report",
        data=merged.to_csv(index=False),
        file_name=f"store_{selected_store}_health.csv"
    )


# Customer Simulation Section
elif section == "🧑‍💼 Customer Simulation":
    st.header("🧑‍💼 Customer Purchase Simulation")

    st.subheader("🎯 Simulated Purchases Across Stores")
    st.dataframe(simulated_customer_data, use_container_width=True)

    st.subheader("📉 Purchase Impact on Stock Levels")
    
    impact_chart = alt.Chart(simulated_customer_data).transform_fold(
    ['Stock Levels', 'Simulated Purchases', 'Updated Stock'],
    as_=['Metric', 'Value']
    ).mark_bar().encode(
        x=alt.X('Product ID:N', title='Product ID'),
        y=alt.Y('Value:Q', title='Units'),
        color=alt.Color('Metric:N', title='Metric'),
        tooltip=[alt.Tooltip('Store ID:N'), alt.Tooltip('Product ID:N'),
                alt.Tooltip('Metric:N'), alt.Tooltip('Value:Q')]
    ).properties(height=350)

    st.altair_chart(impact_chart, use_container_width=True)

    st.download_button(
        label="📥 Download Simulated Customer Impact",
        data=simulated_customer_data.to_csv(index=False),
        file_name="customer_simulation.csv"
    )


# Pricing Insights Section
if section == "💰 Pricing Insights":
    st.header("💰 Pricing Strategy Insights")

    pricing_agent = PricingAgent()
    pricing_data = pricing_agent.data.copy()

    st.subheader("🔍 Product Pricing Table")
    st.dataframe(pricing_data, use_container_width=True)

    st.subheader("🔼 Top 10 Most Expensive Products")
    top_expensive = pricing_data.sort_values(by="Price", ascending=False).head(10)
    bar_expensive = alt.Chart(top_expensive).mark_bar(color="#e15759").encode(
        x=alt.X("Product ID:N", sort="-y"),
        y=alt.Y("Price:Q"),
        tooltip=["Product ID", "Price"]
    ).properties(height=300)
    st.altair_chart(bar_expensive, use_container_width=True)

    st.subheader("🔽 Price Distribution")
    hist = alt.Chart(pricing_data).mark_bar(color="#59a14f").encode(
        alt.X("Price:Q", bin=alt.Bin(maxbins=30)),
        y='count()',
        tooltip=['count()']
    ).properties(height=300)
    st.altair_chart(hist, use_container_width=True)

    st.download_button(
        label="📂 Download Pricing Dataset",
        data=pricing_data.to_csv(index=False),
        file_name="pricing_insights.csv"
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.success("Navigate through each section to explore the system insights.")
