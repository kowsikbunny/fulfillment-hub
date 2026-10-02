# 📦 Fulfillment Hub

An operational control center for managing e-commerce fulfillment, orders, inventory, and operational exceptions.

## Overview

The business is an e-commerce operation that manages order fulfillment using spreadsheets and shared folders. As the business grows, important operational problems can become difficult to identify and follow up.

Fulfillment Hub provides a simple interface to make these problems visible, prioritize important work, and recommend the next operational action.

The application focuses on five key operational problems:

* Priority order delay risks
* Inventory shortages and stock transfers
* Courier pickup delays
* SKU / variant verification
* Informal or forgotten operational exceptions

## Key Features

### 🏠 Operations Dashboard

The dashboard provides an operational snapshot of the fulfillment process.

It includes:

* Total orders
* High-priority orders
* Pickup delays
* Inventory risks
* Critical exceptions
* Priority Work Queue
* Fulfillment Pipeline
* Courier Pickup Health
* Exception Health

The dashboard is designed around:

**Visibility → Priority → Action**

### 📦 Orders

The Orders page allows the operations team to:

* Search orders
* Filter by priority
* Filter by order status
* Filter by pickup status
* Review operational risk
* View recommended next actions
* Identify critical and high-risk active orders

Completed orders are excluded from the operational Priority Work Queue.

### 📊 Inventory

The Inventory page provides visibility into warehouse stock and order demand.

It includes:

* Main warehouse availability
* Secondary warehouse availability
* Open order demand
* Stock shortfall
* Transfer quantity
* Stock health
* Recommended action
* SKU/Product search
* Category filtering
* Action filtering

This helps identify when stock needs to be transferred from the secondary warehouse or when available stock is insufficient to fulfill demand.

### 🚨 Exceptions

The Exceptions page provides a centralized operational issue queue.

It includes:

* Exception ID
* Order ID
* Issue Type
* Severity
* Status
* Recommended Action
* High-impact exception visibility

Examples of operational exceptions include:

* Priority Order Delay Risk
* Stock Transfer Required
* Courier Pickup Delayed
* SKU / Variant Verification
* Insufficient Stock

## Operational Approach

The application follows a simple workflow:

```text
Problem
   ↓
Visibility
   ↓
Priority
   ↓
Recommended Action
```

The system does not attempt to automatically execute physical warehouse or courier actions. Instead, it identifies operational risks and gives the operations team a clear next action.

## Technology

* Python
* Streamlit
* Pandas
* CSV-based sample datasets

## Project Structure

```text
fulfillment-hub/

│
├── app.py
├── validate_data.py
├── check_data.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── orders.csv
│   ├── products.csv
│   ├── inventory.csv
│   ├── warehouses.csv
│   ├── couriers.csv
│   └── exceptions.csv
│
├── src/
│   └── ...
│
└── docs/
    ├── ai_usage_note.md
    └── video_script.md
```

## Data Validation

Before building the application, the sample data was validated for key operational data-quality issues.

Validation checks include:

* Order status values
* Priority values
* Warehouse assignments
* Pickup status values
* Exception types
* Exception severity
* Unknown SKUs
* Products without inventory
* Duplicate Order IDs
* Duplicate Product SKUs

The validation completed without unknown SKUs, products without inventory, duplicate Order IDs, or duplicate Product SKUs.

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/kowsikbunny/fulfillment-hub.git

cd fulfillment-hub
```

### 2. Install dependencies

Make sure Python 3.13 or a compatible Python version is installed.

Then run:

```bash
python -m pip install -r requirements.txt
```

If Streamlit is not installed:

```bash
python -m pip install streamlit
```

### 3. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Running Data Validation

To validate the sample datasets independently:

```bash
python validate_data.py
```

## Sample Data

The project uses dummy operational data created specifically to demonstrate the fulfillment workflow. No real customer, warehouse, or courier data is used.

## Video Walkthrough

A short walkthrough demonstrates:

1. Problem understanding
2. Operations Dashboard
3. Orders and Priority Work Queue
4. Inventory controls
5. Exception management
6. Operational decision-making

## Project Goal

The goal of Fulfillment Hub is not to create a generic analytics dashboard.

It is designed as an operational control center that helps a fulfillment team:

**Identify → Prioritize → Act**

before operational issues turn into missed fulfillment deadlines or customer-facing errors.
