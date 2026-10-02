import streamlit as st
import pandas as pd
import os


# ---------------------------------------------------------
# SHARED OPERATIONAL RULES
# ---------------------------------------------------------
ACTION_MAP = {
    "Priority Order Delay Risk": "Escalate fulfillment",
    "Stock Transfer Required": "Transfer stock",
    "Insufficient Stock": "Resolve stock shortage",
    "Courier Pickup Delayed": "Contact courier",
    "SKU / Variant Verification": "Verify SKU / variant",
}

SEVERITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Normal": 4,
}


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Fulfillment Hub",
    page_icon="📦",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

DATA_PATH = "data"


@st.cache_data
def load_data():
    orders = pd.read_csv(os.path.join(DATA_PATH, "orders.csv"))
    products = pd.read_csv(os.path.join(DATA_PATH, "products.csv"))
    inventory = pd.read_csv(os.path.join(DATA_PATH, "inventory.csv"))
    warehouses = pd.read_csv(os.path.join(DATA_PATH, "warehouses.csv"))
    couriers = pd.read_csv(os.path.join(DATA_PATH, "couriers.csv"))
    exceptions = pd.read_csv(os.path.join(DATA_PATH, "exceptions.csv"))

    return (
        orders,
        products,
        inventory,
        warehouses,
        couriers,
        exceptions
    )


orders, products, inventory, warehouses, couriers, exceptions = load_data()


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("📦 Fulfillment Hub")

st.sidebar.caption("Operations Control Center")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📦 Orders",
        "📊 Inventory",
        "🚨 Exceptions"
    ]
)

# =========================================================
# DASHBOARD — OPERATIONS CONTROL CENTER
# =========================================================

if page == "🏠 Dashboard":

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.title("📦 Fulfillment Hub")

    st.caption(
        "Operations Control Center · Monitor → Prioritize → Act"
    )

    st.divider()

    # -----------------------------------------------------
    # CORE METRICS
    # -----------------------------------------------------

    total_orders = len(orders)

    open_orders = len(
        orders[
            orders["Order_Status"] != "Shipped"
        ]
    )

    shipped_orders = len(
        orders[
            orders["Order_Status"] == "Shipped"
        ]
    )

    high_priority = len(
        orders[
            (orders["Priority"] == "High")
            & (orders["Order_Status"] != "Shipped")
        ]
    )

    pickup_delayed = len(
        orders[
            orders["Pickup_Status"] == "Pickup Delayed"
        ]
    )

    critical_exceptions = len(
        exceptions[
            exceptions["Severity"] == "Critical"
        ]
    )

    priority_risks = len(
        exceptions[
            exceptions["Issue_Type"]
            == "Priority Order Delay Risk"
        ]
    )

    stock_transfer = len(
        exceptions[
            exceptions["Issue_Type"]
            == "Stock Transfer Required"
        ]
    )

    insufficient_stock = len(
        exceptions[
            exceptions["Issue_Type"]
            == "Insufficient Stock"
        ]
    )

    inventory_issues = (
        stock_transfer +
        insufficient_stock
    )

    sku_verification = len(
        exceptions[
            exceptions["Issue_Type"]
            == "SKU / Variant Verification"
        ]
    )

    # -----------------------------------------------------
    # OPERATIONS SNAPSHOT
    # -----------------------------------------------------

    st.subheader("📊 Operations Snapshot")

    st.caption(
        "A quick view of the fulfillment risks that need monitoring."
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "🔴 Critical",
            critical_exceptions,
            help="Critical exceptions requiring immediate attention."
        )

    with c2:
        st.metric(
            "🟠 Open High Priority",
            high_priority,
            help="High-priority orders that are not yet shipped."
        )

    with c3:
        st.metric(
            "🚚 Pickup Delays",
            pickup_delayed,
            help="Orders currently affected by courier pickup delays."
        )

    with c4:
        st.metric(
            "📦 Inventory Risks",
            inventory_issues,
            help="Orders affected by stock transfer or stock shortage issues."
        )

    with c5:
        st.metric(
            "⏳ Open Orders",
            open_orders,
            help="Orders that have not yet been shipped."
        )

    st.divider()

    # -----------------------------------------------------
    # ACTION CENTER
    # -----------------------------------------------------

    st.subheader("🚨 Action Center")

    st.caption(
        "Focus on these operational issues before they become fulfillment delays."
    )

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.metric(
            "🔴 Critical Exceptions",
            critical_exceptions
        )

        if critical_exceptions > 0:
            st.error(
                "Review critical cases"
            )
        else:
            st.success(
                "No critical cases"
            )

    with a2:

        st.metric(
            "🟠 Priority Delay Risks",
            priority_risks
        )

        if priority_risks > 0:
            st.warning(
                "Escalate priority orders"
            )
        else:
            st.success(
                "No priority delay risks"
            )

    with a3:

        st.metric(
            "🚚 Pickup Delays",
            pickup_delayed
        )

        if pickup_delayed > 0:
            st.warning(
                "Contact affected courier"
            )
        else:
            st.success(
                "Pickup operations normal"
            )

    with a4:

        st.metric(
            "📦 Inventory Risks",
            inventory_issues
        )

        if inventory_issues > 0:
            st.warning(
                "Review stock requirements"
            )
        else:
            st.success(
                "Inventory looks healthy"
            )

    st.divider()

    # -----------------------------------------------------
    # FULFILLMENT PIPELINE
    # -----------------------------------------------------

    st.subheader("📦 Fulfillment Pipeline")

    st.caption(
        "Where orders are currently sitting in the fulfillment process."
    )

    pipeline_statuses = [
        "Received",
        "Processing",
        "Picking",
        "Packing",
        "Staged",
        "Shipped"
    ]

    pipeline_counts = (
        orders["Order_Status"]
        .value_counts()
    )

    pipeline_cols = st.columns(6)

    for col, status in zip(
        pipeline_cols,
        pipeline_statuses
    ):

        count = int(
            pipeline_counts.get(status, 0)
        )

        percentage = (
            count / total_orders * 100
            if total_orders > 0
            else 0
        )

        with col:

            st.markdown(
                f"**{status}**"
            )

            st.metric(
                label="Orders",
                value=count
            )

            st.progress(
                min(percentage / 100, 1.0)
            )

            st.caption(
                f"{percentage:.1f}% of total"
            )

    st.divider()

    # -----------------------------------------------------
    # PRIORITY WORK QUEUE
    # -----------------------------------------------------

    st.subheader("🔥 Priority Work Queue")

    st.caption(
        "High-priority orders that may require immediate operational action."
    )

    priority_orders = orders[
        (orders["Priority"] == "High")
        & (orders["Order_Status"] != "Shipped")
    ].copy()

    if len(priority_orders) > 0:

        # If an order has multiple exceptions, use the highest-severity issue.
        exception_ranked = exceptions.copy()
        exception_ranked["Severity_Order"] = (
            exception_ranked["Severity"]
            .map(SEVERITY_ORDER)
            .fillna(9)
        )
        exception_ranked = (
            exception_ranked
            .sort_values(["Order_ID", "Severity_Order"])
            .groupby("Order_ID", as_index=False)
            .first()
        )

        exception_lookup = exception_ranked[
            ["Order_ID", "Severity", "Issue_Type"]
        ].copy()

        priority_orders = priority_orders.merge(
            exception_lookup,
            on="Order_ID",
            how="left"
        )

        # A high-priority order is operationally important even without an exception.
        priority_orders["Risk"] = (
            priority_orders["Severity"]
            .fillna("High")
        )

        priority_orders["Next Action"] = (
            priority_orders["Issue_Type"]
            .map(ACTION_MAP)
            .fillna("Prioritize fulfillment")
        )

        priority_orders["Risk_Order"] = (
            priority_orders["Risk"]
            .map(SEVERITY_ORDER)
            .fillna(9)
        )

        priority_orders["SLA_Sort"] = pd.to_datetime(
            priority_orders["SLA_Deadline"],
            errors="coerce"
        )

        priority_orders = (
            priority_orders
            .sort_values(["Risk_Order", "SLA_Sort"], na_position="last")
        )

        queue_columns = [
            "Order_ID",
            "Priority",
            "Order_Status",
            "SLA_Deadline",
            "Pickup_Status",
            "Risk",
            "Next Action"
        ]

        queue_df = priority_orders[
            queue_columns
        ].head(10).copy()

        st.dataframe(
            queue_df,
            use_container_width=True,
            hide_index=True,
            height=390
        )

    else:

        st.success(
            "No open high-priority orders currently exist."
        )

    st.divider()

    # -----------------------------------------------------
    # OPERATIONS HEALTH
    # -----------------------------------------------------

    st.subheader("📈 Operations Health")

    h1, h2 = st.columns(2)

    # -----------------------------------------------------
    # PICKUP HEALTH
    # -----------------------------------------------------

    with h1:

        st.subheader("🚚 Courier Pickup Health")

        pickup_counts = (
            orders["Pickup_Status"]
            .value_counts()
            .reset_index()
        )

        pickup_counts.columns = [
            "Pickup Status",
            "Orders"
        ]

        st.dataframe(
            pickup_counts,
            use_container_width=True,
            hide_index=True,
            height=230
        )

        if pickup_delayed > 0:

            st.warning(
                f"{pickup_delayed} orders are currently "
                "waiting on delayed courier pickup."
            )

    # -----------------------------------------------------
    # EXCEPTION HEALTH
    # -----------------------------------------------------

    with h2:

        st.subheader("⚠️ Exception Health")

        exception_counts = (
            exceptions["Issue_Type"]
            .value_counts()
            .reset_index()
        )

        exception_counts.columns = [
            "Issue Type",
            "Cases"
        ]

        st.dataframe(
            exception_counts,
            use_container_width=True,
            hide_index=True,
            height=230
        )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.divider()

    st.caption(
        "Fulfillment Hub helps operations teams identify "
        "high-impact work, prioritize exceptions, and act "
        "before fulfillment deadlines are missed."
    )



# =========================================================
# ORDERS
# =========================================================

elif page == "📦 Orders":

    st.title("📦 Order Management")

    st.caption(
        "Search, prioritize, and identify orders that need "
        "operational attention."
    )

    st.divider()

    # -----------------------------------------------------
    # BUILD ORDER RISK INFORMATION
    # -----------------------------------------------------

    order_view = orders.copy()

    # Get exceptions related to each order
    exception_ranked = exceptions.copy()
    exception_ranked["Severity_Order"] = (
        exception_ranked["Severity"]
        .map(SEVERITY_ORDER)
        .fillna(9)
    )

    exception_summary = (
        exception_ranked
        .sort_values(["Order_ID", "Severity_Order"])
        .groupby("Order_ID", as_index=False)
        .agg(
            Max_Severity=("Severity", "first"),
            Issue_Count=("Exception_ID", "count"),
            Primary_Issue=("Issue_Type", "first")
        )
    )

    order_view = order_view.merge(
        exception_summary,
        on="Order_ID",
        how="left"
    )

    order_view["Issue_Count"] = (
        order_view["Issue_Count"]
        .fillna(0)
        .astype(int)
    )

    # -----------------------------------------------------
    # DETERMINE OPERATIONAL RISK
    # -----------------------------------------------------

    def determine_risk(row):

        if pd.notna(row["Max_Severity"]):
            return row["Max_Severity"]

        if row["Priority"] == "High":
            return "High"

        if row["Pickup_Status"] == "Pickup Delayed":
            return "Medium"

        return "Normal"


    order_view["Operational Risk"] = (
        order_view.apply(
            determine_risk,
            axis=1
        )
    )

    # -----------------------------------------------------
    # DETERMINE NEXT ACTION
    # -----------------------------------------------------

    def determine_action(row):

        if pd.notna(row["Primary_Issue"]):
            return ACTION_MAP.get(
                row["Primary_Issue"],
                "Review exception"
            )

        if row["Priority"] == "High":
            return "Prioritize fulfillment"

        if row["Pickup_Status"] == "Pickup Delayed":
            return "Contact courier"

        return "No immediate action"


    order_view["Next Action"] = (
        order_view.apply(
            determine_action,
            axis=1
        )
    )

    # -----------------------------------------------------
    # ORDER SUMMARY
    # -----------------------------------------------------

    total_orders = len(order_view)

    orders_needing_attention = len(
        order_view[
            order_view["Operational Risk"].isin(
                ["Critical", "High", "Medium"]
            )
        ]
    )

    critical_orders = len(
        order_view[
            order_view["Operational Risk"] == "Critical"
        ]
    )

    high_risk_orders = len(
        order_view[
            order_view["Operational Risk"] == "High"
        ]
    )

    pickup_delayed_orders = len(
        order_view[
            order_view["Pickup_Status"] == "Pickup Delayed"
        ]
    )

    st.subheader("Order Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Orders",
            total_orders
        )

    with col2:
        st.metric(
            "Needs Attention",
            orders_needing_attention
        )

    with col3:
        st.metric(
            "High Risk",
            high_risk_orders
        )

    with col4:
        st.metric(
            "Pickup Delayed",
            pickup_delayed_orders
        )

    st.divider()

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    st.subheader("🔎 Find Orders")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        order_search = st.text_input(
            "Search Order / SKU / Product",
            placeholder="Example: ORD-0001"
        )

    with filter_col2:

        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "High",
                "Normal"
            ]
        )

    with filter_col3:

        risk_filter = st.selectbox(
            "Operational Risk",
            [
                "All",
                "Critical",
                "High",
                "Medium",
                "Normal"
            ]
        )

    filter_col4, filter_col5, filter_col6 = st.columns(3)

    with filter_col4:

        status_filter = st.selectbox(
            "Order Status",
            ["All"] + sorted(
                order_view["Order_Status"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with filter_col5:

        pickup_filter = st.selectbox(
            "Pickup Status",
            ["All"] + sorted(
                order_view["Pickup_Status"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with filter_col6:

        courier_filter = st.selectbox(
            "Courier",
            ["All"] + sorted(
                order_view["Courier_Name"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered_orders = order_view.copy()

    if order_search:

        search_text = order_search.strip()

        filtered_orders = filtered_orders[
            filtered_orders["Order_ID"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered_orders["SKU"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered_orders["Product_Name"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if priority_filter != "All":

        filtered_orders = filtered_orders[
            filtered_orders["Priority"]
            == priority_filter
        ]

    if risk_filter != "All":

        filtered_orders = filtered_orders[
            filtered_orders["Operational Risk"]
            == risk_filter
        ]

    if status_filter != "All":

        filtered_orders = filtered_orders[
            filtered_orders["Order_Status"]
            == status_filter
        ]

    if pickup_filter != "All":

        filtered_orders = filtered_orders[
            filtered_orders["Pickup_Status"]
            == pickup_filter
        ]

    if courier_filter != "All":

        filtered_orders = filtered_orders[
            filtered_orders["Courier_Name"]
            == courier_filter
        ]

    # -----------------------------------------------------
    # RESULT COUNT
    # -----------------------------------------------------

    st.write(
        f"**Showing {len(filtered_orders)} "
        f"of {len(order_view)} orders**"
    )

    # -----------------------------------------------------
    # ORDER TABLE
    # -----------------------------------------------------

    display_columns = [
        "Order_ID",
        "Order_Date",
        "Priority",
        "SKU",
        "Product_Name",
        "Variant",
        "Quantity",
        "Order_Status",
        "SLA_Deadline",
        "Courier_Name",
        "Pickup_Status",
        "Operational Risk",
        "Next Action"
    ]

    st.dataframe(
        filtered_orders[display_columns],
        use_container_width=True,
        hide_index=True,
        height=560
    )

  # -----------------------------------------------------
# PRIORITY WORK QUEUE
# -----------------------------------------------------

    st.divider()

    st.subheader("🚨 Priority Work Queue")

    priority_queue = order_view[
       order_view["Operational Risk"].isin(
        ["Critical", "High"]
    )
    ].copy()

# -----------------------------------------------------
# REMOVE ORDERS THAT NO LONGER NEED FULFILLMENT ACTION
# -----------------------------------------------------

    priority_queue = priority_queue[
    ~priority_queue["Order_Status"].isin(
        ["Shipped", "Cancelled", "Delivered"]
    )
].copy()

    if len(priority_queue) > 0:

     risk_order = {
        "Critical": 1,
        "High": 2
    }

     priority_queue["Risk_Order"] = (
        priority_queue["Operational Risk"]
        .map(risk_order)
        .fillna(3)
    )

     priority_queue = (
        priority_queue
        .sort_values(
            ["Risk_Order", "SLA_Deadline"]
            if "SLA_Deadline" in priority_queue.columns
            else ["Risk_Order"]
        )
        .drop(columns=["Risk_Order"])
    )

     queue_columns = [
        "Order_ID",
        "Priority",
        "Order_Status",
        "Pickup_Status",
        "Operational Risk",
        "Next Action"
    ]

     st.dataframe(
        priority_queue[queue_columns].head(10),
        use_container_width=True,
        hide_index=True,
        height=350
    )

    else:

     st.success(
        "No critical or high-risk orders require attention."
    )

# =========================================================
# INVENTORY
# =========================================================

elif page == "📊 Inventory":

    st.title("📊 Inventory Control")

    st.caption(
        "Monitor stock, compare current demand, and identify "
        "the action required to prevent fulfillment delays."
    )

    st.divider()

    # -----------------------------------------------------
    # INVENTORY DATA
    # -----------------------------------------------------

    main_inventory = inventory[
        inventory["Warehouse_ID"] == "WH-MAIN"
    ][
        [
            "SKU",
            "Stock_On_Hand",
            "Reserved",
            "Available_Stock"
        ]
    ].copy()

    main_inventory = main_inventory.rename(
        columns={
            "Stock_On_Hand": "Main Stock",
            "Reserved": "Reserved",
            "Available_Stock": "Main Available"
        }
    )

    secondary_inventory = inventory[
        inventory["Warehouse_ID"] == "WH-SECONDARY"
    ][
        [
            "SKU",
            "Available_Stock"
        ]
    ].copy()

    secondary_inventory = secondary_inventory.rename(
        columns={
            "Available_Stock": "Secondary Available"
        }
    )

    # -----------------------------------------------------
    # OPEN ORDER DEMAND
    # -----------------------------------------------------

    open_orders = orders[
        orders["Order_Status"] != "Shipped"
    ].copy()

    open_demand = (
        open_orders
        .groupby("SKU", as_index=False)["Quantity"]
        .sum()
        .rename(
            columns={
                "Quantity": "Open Order Demand"
            }
        )
    )

    # -----------------------------------------------------
    # COMBINE DATA
    # -----------------------------------------------------

    inventory_view = (
        main_inventory
        .merge(
            secondary_inventory,
            on="SKU",
            how="left"
        )
        .merge(
            open_demand,
            on="SKU",
            how="left"
        )
        .merge(
            products[
                [
                    "SKU",
                    "Product_Name",
                    "Category",
                    "Variant"
                ]
            ],
            on="SKU",
            how="left"
        )
    )

    inventory_view["Open Order Demand"] = (
        inventory_view["Open Order Demand"]
        .fillna(0)
    )

    inventory_view["Secondary Available"] = (
        inventory_view["Secondary Available"]
        .fillna(0)
    )

    # -----------------------------------------------------
    # LOW STOCK THRESHOLD
    # -----------------------------------------------------

    st.subheader("Inventory Risk Controls")

    threshold_col1, threshold_col2 = st.columns(2)

    with threshold_col1:

        low_stock_threshold = st.number_input(
            "Low-stock threshold (Main Available)",
            min_value=1,
            max_value=20,
            value=5,
            step=1
        )

    with threshold_col2:

        st.caption(
            "A SKU is considered low stock when main "
            "warehouse available stock is at or below "
            "the selected threshold."
        )

    # -----------------------------------------------------
    # CALCULATE SHORTFALL AND ACTION
    # -----------------------------------------------------

    inventory_view["Shortfall"] = (
        inventory_view["Open Order Demand"]
        - inventory_view["Main Available"]
    ).clip(lower=0)

    def determine_action(row):

        if row["Shortfall"] <= 0:
            return "Stock Available"

        elif row["Secondary Available"] >= row["Shortfall"]:
            return "Transfer Required"

        else:
            return "Insufficient Stock"

    inventory_view["Action"] = (
        inventory_view.apply(
            determine_action,
            axis=1
        )
    )

    # -----------------------------------------------------
    # STOCK HEALTH
    # -----------------------------------------------------

    def determine_stock_health(row):

        if row["Main Available"] <= 0:
            return "Critical"

        elif row["Main Available"] <= low_stock_threshold:
            return "Low"

        else:
            return "Healthy"

    inventory_view["Stock Health"] = (
        inventory_view.apply(
            determine_stock_health,
            axis=1
        )
    )

    # -----------------------------------------------------
    # RECOMMENDED TRANSFER QUANTITY
    # -----------------------------------------------------

    inventory_view["Transfer Qty"] = (
        inventory_view["Shortfall"]
        .where(
            inventory_view["Action"] == "Transfer Required",
            0
        )
    )

    # -----------------------------------------------------
    # SUMMARY METRICS
    # -----------------------------------------------------

    total_skus = len(inventory_view)

    stock_available = len(
        inventory_view[
            inventory_view["Action"] == "Stock Available"
        ]
    )

    transfer_required = len(
        inventory_view[
            inventory_view["Action"] == "Transfer Required"
        ]
    )

    insufficient_stock = len(
        inventory_view[
            inventory_view["Action"] == "Insufficient Stock"
        ]
    )

    low_stock = len(
        inventory_view[
            inventory_view["Stock Health"] == "Low"
        ]
    )

    critical_stock = len(
        inventory_view[
            inventory_view["Stock Health"] == "Critical"
        ]
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    st.subheader("Inventory Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total SKUs",
            total_skus
        )

    with col2:
        st.metric(
            "Stock Available",
            stock_available
        )

    with col3:
        st.metric(
            "Transfer Required",
            transfer_required
        )

    with col4:
        st.metric(
            "Low Stock",
            low_stock
        )

    with col5:
        st.metric(
            "Insufficient Stock",
            insufficient_stock
        )

    if critical_stock > 0:
        st.warning(
            f"⚠️ {critical_stock} SKU(s) have zero "
            "available stock in the main warehouse."
        )

    st.divider()

    # -----------------------------------------------------
    # SEARCH AND FILTERS
    # -----------------------------------------------------

    st.subheader("🔎 Find Inventory Issues")

    search_col, category_col, action_col = st.columns(3)

    with search_col:

        inventory_search = st.text_input(
            "Search SKU or Product",
            placeholder="Example: SKU-019 or Laptop Backpack"
        )

    with category_col:

        categories = sorted(
            inventory_view["Category"]
            .dropna()
            .unique()
            .tolist()
        )

        category_filter = st.selectbox(
            "Category",
            ["All"] + categories
        )

    with action_col:

        action_filter = st.selectbox(
            "Action",
            [
                "All",
                "Transfer Required",
                "Insufficient Stock",
                "Stock Available"
            ]
        )

    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered_inventory = inventory_view.copy()

    if inventory_search:

        search_text = inventory_search.strip()

        filtered_inventory = filtered_inventory[
            filtered_inventory["SKU"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered_inventory["Product_Name"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if category_filter != "All":

        filtered_inventory = filtered_inventory[
            filtered_inventory["Category"]
            == category_filter
        ]

    if action_filter != "All":

        filtered_inventory = filtered_inventory[
            filtered_inventory["Action"]
            == action_filter
        ]

    # -----------------------------------------------------
    # RESULT COUNT
    # -----------------------------------------------------

    st.write(
        f"**Showing {len(filtered_inventory)} "
        f"of {len(inventory_view)} SKUs**"
    )

    # -----------------------------------------------------
    # OPERATIONAL TABLE
    # -----------------------------------------------------

    display_columns = [
        "SKU",
        "Product_Name",
        "Variant",
        "Main Available",
        "Secondary Available",
        "Open Order Demand",
        "Shortfall",
        "Transfer Qty",
        "Stock Health",
        "Action"
    ]

    st.dataframe(
        filtered_inventory[display_columns],
        use_container_width=True,
        hide_index=True,
        height=520
    )

    st.caption(
        "Shortfall represents the quantity not covered by "
        "available main-warehouse stock. Transfer Qty shows "
        "the quantity recommended from the secondary warehouse."
    )

# =========================================================
# EXCEPTIONS — EXCEPTION COMMAND CENTER
# =========================================================

elif page == "🚨 Exceptions":

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.title("🚨 Exception Command Center")

    st.caption(
        "Identify operational issues, understand their impact, "
        "and determine the next action."
    )

    st.divider()

    # -----------------------------------------------------
    # CORE EXCEPTION METRICS
    # -----------------------------------------------------

    total_exceptions = len(exceptions)

    critical_count = len(
        exceptions[
            exceptions["Severity"] == "Critical"
        ]
    )

    high_count = len(
        exceptions[
            exceptions["Severity"] == "High"
        ]
    )

    medium_count = len(
        exceptions[
            exceptions["Severity"] == "Medium"
        ]
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    st.subheader("📊 Exception Overview")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Total Exceptions",
            total_exceptions
        )

    with m2:
        st.metric(
            "🔴 Critical",
            critical_count
        )

    with m3:
        st.metric(
            "🟠 High",
            high_count
        )

    with m4:
        st.metric(
            "🟡 Medium",
            medium_count
        )

    st.divider()

    # -----------------------------------------------------
    # ACTION SUMMARY
    # -----------------------------------------------------

    st.subheader("🎯 Operational Action Summary")

    st.caption(
        "Group exceptions by the action required to resolve them."
    )

    action_summary = (
        exceptions["Issue_Type"]
        .value_counts()
        .reset_index()
    )

    action_summary.columns = [
        "Issue Type",
        "Cases"
    ]

    action_summary["Recommended Action"] = (
        action_summary["Issue Type"]
        .map(ACTION_MAP)
        .fillna("Review exception")
    )

    st.dataframe(
        action_summary,
        use_container_width=True,
        hide_index=True,
        height=260
    )

    st.divider()

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    st.subheader("🔎 Find Exceptions")

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:

        exception_search = st.text_input(
            "Search Order / Exception",
            placeholder="Example: ORD-0001"
        )

    with filter_col2:

        severity_filter = st.selectbox(
            "Severity",
            [
                "All",
                "Critical",
                "High",
                "Medium"
            ]
        )

    with filter_col3:

        issue_filter = st.selectbox(
            "Issue Type",
            ["All"] +
            sorted(
                exceptions["Issue_Type"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with filter_col4:

        status_filter = st.selectbox(
            "Status",
            ["All"] +
            sorted(
                exceptions["Status"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered_exceptions = exceptions.copy()

    if exception_search:

        search_text = exception_search.strip()

        filtered_exceptions = filtered_exceptions[
            filtered_exceptions["Order_ID"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered_exceptions["Exception_ID"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if severity_filter != "All":

        filtered_exceptions = filtered_exceptions[
            filtered_exceptions["Severity"]
            == severity_filter
        ]

    if issue_filter != "All":

        filtered_exceptions = filtered_exceptions[
            filtered_exceptions["Issue_Type"]
            == issue_filter
        ]

    if status_filter != "All":

        filtered_exceptions = filtered_exceptions[
            filtered_exceptions["Status"]
            == status_filter
        ]

    # -----------------------------------------------------
    # RESULT COUNT
    # -----------------------------------------------------

    st.write(
        f"**Showing {len(filtered_exceptions)} "
        f"of {len(exceptions)} exceptions**"
    )

    # -----------------------------------------------------
    # PREPARE DISPLAY DATA
    # -----------------------------------------------------

    exception_display = filtered_exceptions.copy()

    exception_display["Recommended Action"] = (
        exception_display["Issue_Type"]
        .map(ACTION_MAP)
        .fillna("Review exception")
    )

    # -----------------------------------------------------
    # PRIORITY ORDER
    # -----------------------------------------------------

    severity_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3
    }

    exception_display["Severity_Order"] = (
        exception_display["Severity"]
        .map(severity_order)
        .fillna(4)
    )

    exception_display = (
        exception_display
        .sort_values("Severity_Order")
        .drop(columns=["Severity_Order"])
    )

    # -----------------------------------------------------
    # EXCEPTION TABLE
    # -----------------------------------------------------

    st.subheader("📋 Exception Queue")

    display_columns = [
        "Exception_ID",
        "Order_ID",
        "Issue_Type",
        "Severity",
        "Status",
        "Recommended Action"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in exception_display.columns
    ]

    st.dataframe(
        exception_display[available_columns],
        use_container_width=True,
        hide_index=True,
        height=430
    )

    st.divider()

    # -----------------------------------------------------
    # HIGH IMPACT CASES
    # -----------------------------------------------------

    st.subheader("🔥 High-Impact Exceptions")

    high_impact = filtered_exceptions[
        filtered_exceptions["Severity"]
        .isin(["Critical", "High"])
    ].copy()

    if len(high_impact) > 0:

        high_impact["Recommended Action"] = (
            high_impact["Issue_Type"]
            .map(ACTION_MAP)
            .fillna("Review exception")
        )

        high_impact["Severity_Order"] = (
            high_impact["Severity"]
            .map(severity_order)
            .fillna(4)
        )

        high_impact = (
            high_impact
            .sort_values("Severity_Order")
            .drop(columns=["Severity_Order"])
        )

        high_impact_columns = [
            "Exception_ID",
            "Order_ID",
            "Issue_Type",
            "Severity",
            "Recommended Action"
        ]

        high_impact_columns = [
            column
            for column in high_impact_columns
            if column in high_impact.columns
        ]

        st.dataframe(
            high_impact[
                high_impact_columns
            ].head(10),
            use_container_width=True,
            hide_index=True,
            height=320
        )

    else:

        st.success(
            "✅ No critical or high-severity exceptions "
            "match the selected filters."
        )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.divider()

    st.caption(
        "Exception Command Center helps operations teams "
        "move from issue detection to a clear recommended operational action."
    )