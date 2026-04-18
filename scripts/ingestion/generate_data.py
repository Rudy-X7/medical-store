import pandas as pd
import random
import os

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
from datetime import datetime, timedelta

# Generate customers
customers = []
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

for i in range(1, 1001):
    customers.append([
        i,
        f"Customer_{i}",
        random.randint(18, 70),
        random.choice(cities)
    ])

df_customers = pd.DataFrame(customers, columns=[
    "customer_id", "name", "age", "city"
])

# Medicines
medicines = [
    ("Paracetamol", "Painkiller"),
    ("Aspirin", "Painkiller"),
    ("Ibuprofen", "Anti-inflammatory"),
    ("Amoxicillin", "Antibiotic"),
    ("Cough Syrup", "Cold")
]

# Generate bills
bills = []
start_date = datetime.now()

for i in range(1, 20001):  # 🔥 20K records
    med, category = random.choice(medicines)
    quantity = random.randint(1, 5)
    price = random.randint(20, 200)

    bills.append([
        i,
        random.randint(1, 1000),
        med,
        category,
        quantity,
        price,
        quantity * price,
        start_date - timedelta(days=random.randint(0, 60))
    ])

df_bills = pd.DataFrame(bills, columns=[
    "bill_id", "customer_id", "medicine", "category",
    "quantity", "price", "total", "date"
])

# Save
df_customers.to_csv("data/raw/customers.csv", index=False)
df_bills.to_csv("data/raw/bills.csv", index=False)

print("✅ Big dataset generated!")

