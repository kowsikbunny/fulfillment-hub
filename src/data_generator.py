from pathlib import Path
from datetime import datetime, timedelta
import csv
import random


# ============================================================
# Configuration
# ============================================================

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

BASE_DATE = datetime(2026, 9, 28, 9, 0, 0)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


# ============================================================
# Master Data
# ============================================================

PRODUCT_NAMES = [
    "Classic Cotton T-Shirt",
    "Premium Running Shoes",
    "Wireless Mouse",
    "Bluetooth Speaker",
    "Laptop Backpack",
    "Stainless Steel Bottle",
    "USB-C Charger",
    "Desk Organizer",
    "Cotton Bedsheet",
    "Travel Pouch",
]

CATEGORIES = [
    "Apparel",
    "Footwear",
    "Electronics",
    "Accessories",
    "Home",
]

VARIANTS = [
    "Black",
    "White",
    "Blue",
    "Red",
    "Green",
    "Large",
    "Medium",
    "Small",
]

WAREHOUSES = [
    {
        "Warehouse_ID": "WH-MAIN",
        "Warehouse_Name": "Main Warehouse",
        "Location": "Hyderabad",
        "Type": "Main",
    },
    {
        "Warehouse_ID": "WH-SECONDARY",
        "Warehouse_Name": "Secondary Warehouse",
        "Location": "Hyderabad",
        "Type": "Secondary",
    },
]

COURIERS = [
    {
        "Courier_ID": "CR-01",
        "Courier_Name": "Delhivery",
        "Pickup_Time": "17:00",
        "Cost": 55,
        "Expected_Delivery_Days": 2,
    },
    {
        "Courier_ID": "CR-02",
        "Courier_Name": "Blue Dart",
        "Pickup_Time": "16:30",
        "Cost": 75,
        "Expected_Delivery_Days": 1,
    },
    {
        "Courier_ID": "CR-03",
        "Courier_Name": "DTDC",
        "Pickup_Time": "18:00",
        "Cost": 50,
        "Expected_Delivery_Days": 3,
    },
    {
        "Courier_ID": "CR-04",
        "Courier_Name": "Ecom Express",
        "Pickup_Time": "17:30",
        "Cost": 48,
        "Expected_Delivery_Days": 2,
    },
]


# ============================================================
# Helper
# ============================================================

def write_csv(filename, rows, fieldnames):
    path = DATA_DIR / filename

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {path}")


# ============================================================
# 1. Products
# ============================================================

def generate_products():
    products = []

    for i in range(1, 51):
        product_name = random.choice(PRODUCT_NAMES)
        variant = random.choice(VARIANTS)
        category = random.choice(CATEGORIES)

        products.append(
            {
                "SKU": f"SKU-{i:03d}",
                "Product_Name": product_name,
                "Category": category,
                "Variant": variant,
                "Unit_Price": random.choice(
                    [299, 399, 499, 599, 799, 999, 1299, 1599, 1999]
                ),
            }
        )

    write_csv(
        "products.csv",
        products,
        [
            "SKU",
            "Product_Name",
            "Category",
            "Variant",
            "Unit_Price",
        ],
    )

    return products


# ============================================================
# 2. Warehouses
# ============================================================

def generate_warehouses():
    write_csv(
        "warehouses.csv",
        WAREHOUSES,
        [
            "Warehouse_ID",
            "Warehouse_Name",
            "Location",
            "Type",
        ],
    )


# ============================================================
# 3. Couriers
# ============================================================

def generate_couriers():
    write_csv(
        "couriers.csv",
        COURIERS,
        [
            "Courier_ID",
            "Courier_Name",
            "Pickup_Time",
            "Cost",
            "Expected_Delivery_Days",
        ],
    )


# ============================================================
# 4. Inventory
# ============================================================

def generate_inventory(products):
    inventory = []

    for product in products:

        # Most products have reasonable main stock
        main_stock = random.randint(5, 35)

        # Some products intentionally have low/no main stock
        if random.random() < 0.20:
            main_stock = random.choice([0, 1, 2, 3])

        # Secondary warehouse keeps additional stock
        secondary_stock = random.randint(0, 30)

        inventory.append(
            {
                "SKU": product["SKU"],
                "Warehouse_ID": "WH-MAIN",
                "Stock_On_Hand": main_stock,
                "Reserved": 0,
                "Available_Stock": main_stock,
            }
        )

        inventory.append(
            {
                "SKU": product["SKU"],
                "Warehouse_ID": "WH-SECONDARY",
                "Stock_On_Hand": secondary_stock,
                "Reserved": 0,
                "Available_Stock": secondary_stock,
            }
        )

    write_csv(
        "inventory.csv",
        inventory,
        [
            "SKU",
            "Warehouse_ID",
            "Stock_On_Hand",
            "Reserved",
            "Available_Stock",
        ],
    )

    return inventory


# ============================================================
# 5. Orders
# ============================================================

def generate_orders(products, inventory, order_count=150):
    orders = []

    # Build quick inventory lookup
    main_stock = {
        row["SKU"]: row["Available_Stock"]
        for row in inventory
        if row["Warehouse_ID"] == "WH-MAIN"
    }

    secondary_stock = {
        row["SKU"]: row["Available_Stock"]
        for row in inventory
        if row["Warehouse_ID"] == "WH-SECONDARY"
    }

    statuses = [
        "Received",
        "Processing",
        "Picking",
        "Packing",
        "Staged",
        "Shipped",
    ]

    customers = [
        "Rahul",
        "Priya",
        "Arjun",
        "Sneha",
        "Vikram",
        "Ananya",
        "Ravi",
        "Neha",
        "Kiran",
        "Suresh",
    ]

    for i in range(1, order_count + 1):

        product = random.choice(products)
        sku = product["SKU"]

        quantity = random.randint(1, 3)

        # Around 20% priority orders
        priority = "High" if random.random() < 0.20 else "Normal"

        order_datetime = BASE_DATE - timedelta(
            days=random.randint(0, 2),
            hours=random.randint(0, 8),
            minutes=random.randint(0, 59),
        )

        # Priority orders have shorter SLA
        if priority == "High":
            sla_deadline = order_datetime + timedelta(hours=8)
        else:
            sla_deadline = order_datetime + timedelta(hours=24)

        status = random.choice(statuses)

        courier = random.choice(COURIERS)

        # Create intentional operational situations
        main_available = main_stock.get(sku, 0)
        secondary_available = secondary_stock.get(sku, 0)

        # All orders ship from the main warehouse.
        # If main stock is unavailable, inventory transfer may be required.
        warehouse = "WH-MAIN"

        pickup_status = "Not Ready"

        if status == "Staged":
            pickup_status = random.choice(
                [
                    "Ready for Pickup",
                    "Ready for Pickup",
                    "Pickup Delayed",
                ]
            )

        elif status == "Shipped":
            pickup_status = "Picked Up"

        orders.append(
            {
                "Order_ID": f"ORD-{i:04d}",
                "Order_Date": order_datetime.strftime("%Y-%m-%d"),
                "Order_Time": order_datetime.strftime("%H:%M"),
                "Priority": priority,
                "Customer": random.choice(customers),
                "SKU": sku,
                "Product_Name": product["Product_Name"],
                "Variant": product["Variant"],
                "Quantity": quantity,
                "Warehouse": warehouse,
                "Order_Status": status,
                "SLA_Deadline": sla_deadline.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "Courier_ID": courier["Courier_ID"],
                "Courier_Name": courier["Courier_Name"],
                "Shipping_Cost": courier["Cost"],
                "Pickup_Status": pickup_status,
            }
        )

    write_csv(
        "orders.csv",
        orders,
        [
            "Order_ID",
            "Order_Date",
            "Order_Time",
            "Priority",
            "Customer",
            "SKU",
            "Product_Name",
            "Variant",
            "Quantity",
            "Warehouse",
            "Order_Status",
            "SLA_Deadline",
            "Courier_ID",
            "Courier_Name",
            "Shipping_Cost",
            "Pickup_Status",
        ],
    )

    return orders


# ============================================================
# 6. Exceptions
# ============================================================

def generate_exceptions(orders, inventory):
    exceptions = []

    exception_id = 1

    main_stock = {
        row["SKU"]: row["Available_Stock"]
        for row in inventory
        if row["Warehouse_ID"] == "WH-MAIN"
    }

    secondary_stock = {
        row["SKU"]: row["Available_Stock"]
        for row in inventory
        if row["Warehouse_ID"] == "WH-SECONDARY"
    }

    # Inventory exceptions
    for order in orders:

        sku = order["SKU"]
        quantity = order["Quantity"]

        main_available = main_stock.get(sku, 0)
        secondary_available = secondary_stock.get(sku, 0)

        if main_available < quantity:

            if secondary_available >= quantity:

                exceptions.append(
                    {
                        "Exception_ID": f"EX-{exception_id:04d}",
                        "Order_ID": order["Order_ID"],
                        "Issue_Type": "Stock Transfer Required",
                        "Severity": "High",
                        "Description": (
                            f"{quantity} unit(s) available in secondary warehouse "
                            "but not enough stock in main warehouse."
                        ),
                        "Status": "Open",
                        "Created_Time": order["Order_Date"]
                        + " "
                        + order["Order_Time"],
                    }
                )

                exception_id += 1

            else:

                exceptions.append(
                    {
                        "Exception_ID": f"EX-{exception_id:04d}",
                        "Order_ID": order["Order_ID"],
                        "Issue_Type": "Insufficient Stock",
                        "Severity": "Critical",
                        "Description": (
                            "Required stock is not available "
                            "across the warehouses."
                        ),
                        "Status": "Open",
                        "Created_Time": order["Order_Date"]
                        + " "
                        + order["Order_Time"],
                    }
                )

                exception_id += 1

    # Priority order exceptions
    for order in orders:

        if order["Priority"] == "High" and order["Order_Status"] not in [
            "Shipped",
            "Staged",
        ]:

            exceptions.append(
                {
                    "Exception_ID": f"EX-{exception_id:04d}",
                    "Order_ID": order["Order_ID"],
                    "Issue_Type": "Priority Order Delay Risk",
                    "Severity": "High",
                    "Description": (
                        "Priority order has not reached shipping stage "
                        "within the expected workflow."
                    ),
                    "Status": "Open",
                    "Created_Time": order["Order_Date"]
                    + " "
                    + order["Order_Time"],
                }
            )

            exception_id += 1

    # Pickup exceptions
    for order in orders:

        if order["Pickup_Status"] == "Pickup Delayed":

            exceptions.append(
                {
                    "Exception_ID": f"EX-{exception_id:04d}",
                    "Order_ID": order["Order_ID"],
                    "Issue_Type": "Courier Pickup Delayed",
                    "Severity": "Medium",
                    "Description": (
                        "Packed order is staged but courier pickup "
                        "has been delayed."
                    ),
                    "Status": "Open",
                    "Created_Time": order["Order_Date"]
                    + " "
                    + order["Order_Time"],
                }
            )

            exception_id += 1

    # SKU / variant exceptions
    sku_issue_orders = random.sample(
        orders,
        min(5, len(orders)),
    )

    for order in sku_issue_orders:

        exceptions.append(
            {
                "Exception_ID": f"EX-{exception_id:04d}",
                "Order_ID": order["Order_ID"],
                "Issue_Type": "SKU / Variant Verification",
                "Severity": "Medium",
                "Description": (
                    "Product or variant should be verified before packing."
                ),
                "Status": "Open",
                "Created_Time": order["Order_Date"]
                + " "
                + order["Order_Time"],
            }
        )

        exception_id += 1

    write_csv(
        "exceptions.csv",
        exceptions,
        [
            "Exception_ID",
            "Order_ID",
            "Issue_Type",
            "Severity",
            "Description",
            "Status",
            "Created_Time",
        ],
    )

    return exceptions


# ============================================================
# Main
# ============================================================

def main():

    print("\nGenerating Fulfillment Hub sample data...\n")

    products = generate_products()

    generate_warehouses()

    generate_couriers()

    inventory = generate_inventory(products)

    orders = generate_orders(
        products,
        inventory,
        order_count=150,
    )

    generate_exceptions(
        orders,
        inventory,
    )

    print("\nData generation completed successfully.")
    print(f"Data files saved in: {DATA_DIR}")


if __name__ == "__main__":
    main()