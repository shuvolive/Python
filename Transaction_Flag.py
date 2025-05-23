import pandas as pd

df = pd.read_csv("transactions.csv")
print(df.head())

from datetime import datetime

df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

df["Hour"] = df["Datetime"].dt.hour

print(df[["Transaction_ID", "Datetime", "Hour"]])

amount_threshold = 10000
high_risk_countries = {"RU", "IR", "KP"}
business_hours = (6, 22)

df["Flag_Amount"]  = df["Amount"] > amount_threshold
df["Flag_Country"]  = df["Country"].isin(high_risk_countries)
df["Flag_Hours"] = ~df["Hour"].between(business_hours[0],business_hours[1])

print(df[["Transaction_ID", "Amount", "Country", "Hour", "Flag_Amount", "Flag_Country", "Flag_Hours"]])

df["Date"] = pd.to_datetime(df["Date"])
tx_count = df.groupby(["Customer_ID", "Date"]).size().reset_index(name="Daily_Tx_Count")
df = df.merge(tx_count, on=["Customer_ID", "Date"])
df["Flag_Frequency"] = df["Daily_Tx_Count"] > 3
print(df[["Customer_ID", "Date", "Daily_Tx_Count", "Flag_Frequency"]])

df["Suspicious"] = df[[
    "Flag_Amount",
    "Flag_Country",
    "Flag_Hours",
]].any(axis=1)

suspicious_df = df[df["Suspicious"]]
suspicious_df.to_csv("suspicious_transactions.csv", index=False)
print("\nSuspicious transactions flagged and saved to suspicious_transactions.csv")

