import pandas as pd

# Load CSVs
items = pd.read_csv("dataset/items.csv")
keywords = pd.read_csv("dataset/keywords.csv")
merchant = pd.read_csv("dataset/merchant.csv")
transaction_data = pd.read_csv("dataset/transaction_data.csv")
transaction_items = pd.read_csv("dataset/transaction_items.csv")

# Merge datasets
merged_orders = pd.merge(
    transaction_data,
    transaction_items,
    on=["order_id","merchant_id"]
)

merged_orders = pd.merge(
    merged_orders,
    items,
    on=["item_id","merchant_id"]
)

merged_data = pd.merge(
    merged_orders,
    merchant,
    on="merchant_id"
)

selected_columns = ['order_id', 'order_time', 'driver_arrival_time', 'driver_pickup_time', 'delivery_time', 'order_value', 'eater_id', 'merchant_id', 'item_id', 'cuisine_tag', 'item_name', 'item_price', 'merchant_name', 'join_date', 'city_id']

# Convert date columns
merged_data['order_time'] = pd.to_datetime(merged_data['order_time'])
merchant['join_date'] = pd.to_datetime(merchant['join_date'])

merged_data = pd.DataFrame(merged_data, columns=selected_columns)

# Save cleaned & merged data
merged_data.to_csv("dataset/merged_data.csv", index=False)
