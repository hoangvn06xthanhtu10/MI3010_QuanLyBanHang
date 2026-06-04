import pandas as pd
import random
from datetime import datetime, timedelta

# ======================
# PRODUCTS
# ======================

products = []

for i in range(1, 101):
    products.append({
        "ProductID": i,
        "ProductName": f"Product {i}",
        "Barcode": f"893{i:09d}",
        "Price": random.randint(10000, 100000),
        "StockQuantity": random.randint(50, 500)
    })

products_df = pd.DataFrame(products)

# ======================
# CUSTOMERS
# ======================

customers = []

for i in range(1, 1001):
    customers.append({
        "CustomerID": i,
        "CustomerName": f"Customer {i}",
        "Phone": f"09{random.randint(10000000,99999999)}",
        "LoyaltyPoint": 0
    })

customers_df = pd.DataFrame(customers)

# ======================
# ORDERS
# ======================

orders = []

start_date = datetime(2025, 1, 1)

for i in range(1, 10001):

    random_days = random.randint(0, 364)

    orders.append({
        "OrderID": i,
        "CustomerID": random.randint(1, 1000),
        "OrderDate": start_date + timedelta(days=random_days),
        "TotalAmount": 0
    })

orders_df = pd.DataFrame(orders)

# ======================
# ORDER DETAILS
# ======================

details = []
detail_id = 1

price_lookup = {
    row.ProductID: row.Price
    for _, row in products_df.iterrows()
}

order_totals = {}

for order_id in range(1, 10001):

    num_items = random.randint(3, 5)

    total = 0

    selected_products = random.sample(range(1, 101), num_items)

    for product_id in selected_products:

        qty = random.randint(1, 5)
        price = price_lookup[product_id]

        total += qty * price

        details.append({
            "DetailID": detail_id,
            "OrderID": order_id,
            "ProductID": product_id,
            "Quantity": qty,
            "UnitPrice": price
        })

        detail_id += 1

    order_totals[order_id] = total

details_df = pd.DataFrame(details)

# ======================
# UPDATE ORDER TOTALS
# ======================

orders_df["TotalAmount"] = orders_df["OrderID"].map(order_totals)

# ======================
# UPDATE LOYALTY POINTS
# ======================

customer_points = (
    orders_df.groupby("CustomerID")["TotalAmount"]
    .sum()
    .floordiv(10000)
)

customers_df["LoyaltyPoint"] = (
    customers_df["CustomerID"]
    .map(customer_points)
    .fillna(0)
    .astype(int)
)

# ======================
# EXPORT CSV
# ======================

products_df.to_csv("products.csv", index=False)
customers_df.to_csv("customers.csv", index=False)
orders_df.to_csv("orders.csv", index=False)
details_df.to_csv("order_details.csv", index=False)

print("Done!")