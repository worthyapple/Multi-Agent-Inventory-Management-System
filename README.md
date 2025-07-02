# 📦 Multi-Agent Inventory Management Dashboard

This project implements a multi-agent inventory management system using Python and Streamlit. It simulates realistic operations across the retail supply chain including:

- 📈 **Forecasting Agent**: Predicts product demand using linear regression.
- 🛒 **Store Agent**: Determines if restocking is needed based on predicted demand.
- 🏬 **Warehouse Agent**: Approves or rejects restock requests based on available capacity.
- 🚛 **Supplier Agent**: Restocks warehouses when capacity falls below thresholds.
- 🧑‍💼 **Customer Agent**: Simulates random customer purchases at stores.
- 💰 **Pricing Agent**: Loads pricing optimization data for potential future use.

---

## 🌐 Live Demo
[Click here to open the Streamlit dashboard](https://your-app-name.streamlit.app/)  
*(Deploy via Streamlit Cloud)*

---

## 📁 Folder Structure

multi-agent-inventory-dashboard/
├── agents.py
├── streamlit_app.py
├── requirements.txt
└── data/
├── demand_forecasting.csv
├── inventory_monitoring.csv
└── pricing_optimization.csv


---

## 🚀 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/multi-agent-inventory-dashboard.git
   cd multi-agent-inventory-dashboard
Install dependencies:
pip install -r requirements.txt

Run the dashboard:
streamlit run streamlit_app.py

# 📊 Features
Clean and interactive dashboard UI with real-time analytics

Demand forecasting using historical sales data

Smart restock recommendations per store

Warehouse fulfillment logic

Supplier-led restocking simulation

Customer behavior simulation (randomized purchases)

Pricing strategy preview

# 📌 Technologies Used
Python 3
Streamlit
Pandas / NumPy / scikit-learn
