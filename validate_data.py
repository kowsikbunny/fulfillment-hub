import pandas as pd

orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
inventory = pd.read_csv("data/inventory.csv")
exceptions = pd.read_csv("data/exceptions.csv")

print("=" * 60)
print("FULFILLMENT HUB BUSINESS DATA VALIDATION")
print("=" * 60)

# 1. Order status distribution
print("\n1. ORDER STATUS")
print(orders["Order_Status"].value_counts())

# 2. Priority distribution
print("\n2. PRIORITY")
print(orders["Priority"].value_counts())

# 3. Warehouse distribution
print("\n3. ORDER WAREHOUSE")
print(orders["Warehouse"].value_counts())

# 4. Pickup status
print("\n4. PICKUP STATUS")
print(orders["Pickup_Status"].value_counts())

# 5. Exceptions
print("\n5. EXCEPTIONS")
print(exceptions["Issue_Type"].value_counts())

# 6. Exception severity
print("\n6. EXCEPTION SEVERITY")
print(exceptions["Severity"].value_counts())

# 7. Product/SKU validation
missing_products = ~orders["SKU"].isin(products["SKU"])
print("\n7. ORDERS WITH UNKNOWN SKU:", missing_products.sum())

# 8. Inventory SKU validation
missing_inventory = ~products["SKU"].isin(inventory["SKU"])
print("8. PRODUCTS WITHOUT INVENTORY:", missing_inventory.sum())

# 9. Duplicate Order IDs
print("9. DUPLICATE ORDER IDs:", orders["Order_ID"].duplicated().sum())

# 10. Duplicate SKUs
print("10. DUPLICATE PRODUCT SKUs:", products["SKU"].duplicated().sum())

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)