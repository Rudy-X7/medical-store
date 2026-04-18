import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
bills = pd.read_csv("data/raw/bills.csv")

# Cleaning
customers.drop_duplicates(inplace=True)
bills.drop_duplicates(inplace=True)

customers.fillna({"age": customers["age"].mean()}, inplace=True)
bills.fillna(0, inplace=True)

bills["date"] = pd.to_datetime(bills["date"])

# Feature engineering
bills["discount"] = bills["total"] * 0.1
bills["final_amount"] = bills["total"] - bills["discount"]

# Merge
df = bills.merge(customers, on="customer_id", how="left")

# Aggregations
customer_spending = df.groupby("customer_id")["final_amount"].sum().reset_index()
medicine_sales = df.groupby("medicine")["quantity"].sum().reset_index()

# Save
df.to_csv("data/processed/cleaned_data.csv", index=False)
customer_spending.to_csv("data/processed/customer_spending.csv", index=False)
medicine_sales.to_csv("data/processed/medicine_sales.csv", index=False)

print("✅ Data processed successfully!")
