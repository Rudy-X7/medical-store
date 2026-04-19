import pandas as pd
import random
from datetime import datetime, timedelta
import os

# ---------------------------
# 📁 CREATE FOLDERS (FIX ERROR)
# ---------------------------
os.makedirs("data/raw", exist_ok=True)

# ---------------------------
# 👥 GENERATE CUSTOMERS
# ---------------------------
customers = []
for i in range(1, 201):  # increased to 200 customers
    customers.append([
        i,
        f"Customer_{i}",
        random.randint(18, 70)
    ])

df_customers = pd.DataFrame(
    customers,
    columns=["customer_id", "name", "age"]
)

# ---------------------------
# 💊 MEDICINES
# ---------------------------
medicines = [
    "Paracetamol", "Aspirin", "Ibuprofen",
    "Amoxicillin", "Cough Syrup",
    "Vitamin C", "Antacid", "Insulin"
]

# ---------------------------
# 🌍 CITIES
# ---------------------------
cities = ["Delhi", "Mumbai", "Kolkata", "Bangalore"]

# ---------------------------
# 🧾 GENERATE BILLING DATA
# ---------------------------
bills = []
start_date = datetime.now()

for i in range(1, 5001):  # 5000 transactions (BIG dataset)
    bill_id = i
    customer_id = random.randint(1, 200)
    medicine = random.choice(medicines)
    quantity = random.randint(1, 10)
    price = random.randint(20, 500)
    total = quantity * price
    date = start_date - timedelta(days=random.randint(0, 90))
    city = random.choice(cities)

    bills.append([
        bill_id,
        customer_id,
        medicine,
        quantity,
        price,
        total,
        date,
        city
    ])

df_bills = pd.DataFrame(bills, columns=[
    "bill_id",
    "customer_id",
    "medicine",
    "quantity",
    "price",
    "total",
    "date",
    "city"
])

# ---------------------------
# 💾 SAVE FILES
# ---------------------------
df_customers.to_csv("data/raw/customers.csv", index=False)
df_bills.to_csv("data/raw/bills.csv", index=False)

print("✅ Data generated successfully with cities & large dataset!")

