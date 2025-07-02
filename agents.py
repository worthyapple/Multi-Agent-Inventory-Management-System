import pandas as pd

import pandas as pd

from sklearn.linear_model import LinearRegression

class ForecastingAgent:
    def __init__(self, demand_data):
        self.demand_data = demand_data

    def predict_demand(self):
        df = self.demand_data.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df['DayOfYear'] = df['Date'].dt.dayofyear

        X = df[['DayOfYear']]
        y = df['Sales Quantity']

        model = LinearRegression()
        model.fit(X, y)

        future_days = pd.DataFrame({'DayOfYear': range(1, 366)})
        predictions = model.predict(future_days)

        product_ids = df['Product ID'].unique()[:len(predictions)]
        return pd.DataFrame({
            'Product ID': product_ids,
            'Predicted Demand': predictions[:len(product_ids)]
        })



class StoreAgent:
    def __init__(self, inventory_data, predicted_demand_df):
        self.inventory_data = inventory_data
        self.predicted_demand = predicted_demand_df

    def check_restock_needed(self):
        restock_list = []

        for _, row in self.inventory_data.iterrows():
            product_id = row['Product ID']
            current_stock = row['Stock Levels']

            # Lookup predicted demand
            forecast = self.predicted_demand[self.predicted_demand['Product ID'] == product_id]

            if not forecast.empty:
                predicted_demand = forecast['Predicted Demand'].values[0]

                # Restock if stock is below predicted demand
                if current_stock < predicted_demand:
                    restock_amount = int(predicted_demand - current_stock)
                    restock_list.append({
                        'Product ID': product_id,
                        'Store ID': row['Store ID'],
                        'Current Stock': current_stock,
                        'Needed': restock_amount
                    })

        return restock_list


class PricingAgent:
    def __init__(self):
        self.name = "Pricing Agent"
        self.data = pd.read_csv('data/pricing_optimization.csv')

    def show_data(self):
        print(f"{self.name} data preview:")
        print(self.data.head())


class WarehouseAgent:
    def __init__(self, warehouse_data):
        self.warehouse_data = warehouse_data

    def fulfill_requests(self, restock_requests):
        """Check warehouse stock and fulfill store restock requests."""
        responses = []

        for request in restock_requests:
            product_id = request['Product ID']
            store_id = request['Store ID']
            needed = request['Needed']

            # Find the product in warehouse data
            warehouse_row = self.warehouse_data[
                (self.warehouse_data['Product ID'] == product_id)
            ]

            if not warehouse_row.empty:
                available = warehouse_row.iloc[0]['Warehouse Capacity']

                if available >= needed:
                    status = "Approved"
                    self.warehouse_data.loc[
                        warehouse_row.index, 'Warehouse Capacity'
                    ] -= needed
                else:
                    status = "Rejected (Insufficient stock)"
            else:
                status = "Rejected (Product not found)"

            responses.append({
                'Product ID': product_id,
                'Store ID': store_id,
                'Needed': needed,
                'Status': status
            })

        return responses


class SupplierAgent:
    def __init__(self, lead_time_days=5):
        self.lead_time_days = lead_time_days

    def restock_warehouse(self, warehouse_agent):
        restocked = []
        for idx, row in warehouse_agent.warehouse_data.iterrows():
            if row['Warehouse Capacity'] < 1000:  # threshold
                restock_amount = 1000  # fixed for now
                warehouse_agent.warehouse_data.at[idx, 'Warehouse Capacity'] += restock_amount
                restocked.append({
                    'Product ID': row['Product ID'],
                    'Restocked By': restock_amount,
                    'New Capacity': warehouse_agent.warehouse_data.at[idx, 'Warehouse Capacity'],
                    'Lead Time (days)': self.lead_time_days
                })
        return restocked



class CustomerAgent:
    def __init__(self):
        self.name = "Customer Agent"

    def role(self):
        return "Simulates customer purchases for testing."

