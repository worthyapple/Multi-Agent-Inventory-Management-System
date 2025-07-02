import pandas as pd 
from agents import ForecastingAgent, StoreAgent, WarehouseAgent, SupplierAgent

# Step 1: Load data
demand_data = pd.read_csv("data/demand_forecasting.csv")
store_data = pd.read_csv("data/inventory_monitoring.csv")
warehouse_data = pd.read_csv("data/inventory_monitoring.csv")  # Used as mock warehouse

# Step 2: Forecast demand
forecasting_agent = ForecastingAgent(demand_data)
predicted_demand = forecasting_agent.predict_demand()

print("\n📈 Predicted Demand (sample):")
print(predicted_demand.head())

# Step 3: Store checks inventory using predicted demand
store_agent = StoreAgent(store_data, predicted_demand)
restock_list = store_agent.check_restock_needed()

print("\n🛒 Smart Restock Recommendations:")
for item in restock_list[:5]:  # Print only first 5
    print(item)

# Step 4: Warehouse tries to fulfill restock requests
warehouse_agent = WarehouseAgent(warehouse_data)
unfulfilled_items = warehouse_agent.fulfill_requests(restock_list)

# Step 5: Supplier refills warehouse for unfulfilled items
supplier_agent = SupplierAgent()
restocked_items = supplier_agent.restock_warehouse(warehouse_agent)
