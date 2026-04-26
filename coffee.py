import pandas as pd
import os
import sys
from datetime import date

#──Report───────────────────────────────────────────────
MODE = sys.argv[1] if len(sys.argv) > 1 else "weekly"
TODAY = date.today()

print(f"Running in {MODE} mode for {TODAY}")

# ── Setup ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Load Data ──────────────────────────────────────────────────────────────────
df1 = pd.read_csv(os.path.join(BASE_DIR, "index_1.csv"))
df2 = pd.read_csv(os.path.join(BASE_DIR, "index_2.csv"))

df1["machine"] = "Machine 1"
df2["machine"] = "Machine 2"

sales_df = pd.concat([df1, df2], ignore_index=True)

print(f"Machine 1: {len(df1)} rows")
print(f"Machine 2: {len(df2)} rows")
print(f"Total    : {len(sales_df)} rows")

# ── Clean Data ─────────────────────────────────────────────────────────────────
sales_df = sales_df.dropna(subset=["date", "money", "coffee_name"])
sales_df = sales_df[sales_df["money"] > 0]

print(f"Clean    : {len(sales_df)} rows")

# ──Filter by mode───────────────────────────
if MODE == "daily":
    sales_df = sales_df[sales_df["date"] == pd.Timestamp(TODAY)]
    print(f"Today's rows: {len(sales_df)}")

# ── Feature Engineering ────────────────────────────────────────────────────────
sales_df["date"]        = pd.to_datetime(sales_df["date"])
sales_df["datetime"]    = pd.to_datetime(sales_df["datetime"], format="mixed")
sales_df["hour"]        = sales_df["datetime"].dt.hour
sales_df["day_of_week"] = sales_df["date"].dt.day_name()
sales_df["month"]       = sales_df["date"].dt.to_period("M")

# ── Analysis: aggregate revenue by date, coffee, and weekday ──
DAYS_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

daily = sales_df.groupby("date").agg(
    total_revenue=("money", "sum")
).reset_index()

top_coffees = sales_df.groupby("coffee_name").agg(
    total_revenue=("money", "sum")
).reset_index().sort_values("total_revenue", ascending=False)

day_sales = sales_df.groupby("day_of_week").agg(
    total_revenue=("money", "sum")
).reset_index()
day_sales.columns = ["day", "total_revenue"]
day_sales["day"] = pd.Categorical(day_sales["day"], categories=DAYS_ORDER, ordered=True)
day_sales = day_sales.sort_values("day")

monthly = sales_df.groupby("month").agg(
    total_revenue=("money", "sum")
).reset_index()
monthly["month"] = monthly["month"].astype(str)

hourly = sales_df.groupby("hour").agg(
    total_revenue=("money", "sum")
).reset_index()

machine = sales_df.groupby("machine").agg(
    total_revenue=("money", "sum")
).reset_index()

payment = sales_df.groupby("cash_type").agg(
    total_revenue=("money", "sum")
).reset_index()
payment.columns = ["payment_type", "total_revenue"]

# ── Export to Excel ────────────────────────────────────────────────────────────
with pd.ExcelWriter(os.path.join(BASE_DIR, "coffee_report.xlsx")) as writer:
    daily.to_excel(writer, sheet_name="Daily Revenue", index=False)
    top_coffees.to_excel(writer, sheet_name="Top Coffees", index=False)
    day_sales.to_excel(writer, sheet_name="Best Days", index=False)
    monthly.to_excel(writer, sheet_name="Monthly Summary", index=False)
    hourly.to_excel(writer, sheet_name="Best Hours", index=False)
    machine.to_excel(writer, sheet_name="Machine Comparison", index=False)
    payment.to_excel(writer, sheet_name="Cash vs Card", index=False)

    if MODE == "weekly":
        day_sales.to_excel(writer,   sheet_name="Best Days",          index=False)
        monthly.to_excel(writer,     sheet_name="Monthly Summary",    index=False)
        machine.to_excel(writer,     sheet_name="Machine Comparison", index=False)
        payment.to_excel(writer,     sheet_name="Cash vs Card",       index=False)
    
    # Auto fit column widths
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column if cell.value)
            worksheet.column_dimensions[column[0].column_letter].width = max_length + 4

print("Report saved.")