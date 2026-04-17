import pandas as pd
import numpy as np
from datetime import datetime

def generate_synthetic_expense_data(output_path="data/synthetic_expenses.csv", seed=42):
    np.random.seed(seed)

    start_date = "2025-01-01"
    end_date = "2025-12-31"
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    categories = {
        "Food": (100, 600),
        "Travel": (50, 400),
        "Shopping": (300, 3000),
        "Bills": (500, 2500),
        "Rent": (8000, 15000),
        "Entertainment": (150, 1500),
        "Health": (200, 4000),
        "Education": (500, 5000),
        "Investment": (1000, 10000),
        "Miscellaneous": (100, 2000),
        "Salary": (25000, 60000),
        "Freelance": (2000, 15000),
    }

    expense_categories = [
        "Food", "Travel", "Shopping", "Bills", "Rent",
        "Entertainment", "Health", "Education", "Investment", "Miscellaneous"
    ]
    income_categories = ["Salary", "Freelance"]

    payment_methods = ["UPI", "Cash", "Card", "Bank Transfer"]

    descriptions = {
        "Food": ["Lunch", "Dinner", "Snacks", "Cafe", "Food Delivery"],
        "Travel": ["Bus", "Auto", "Cab", "Fuel", "Train"],
        "Shopping": ["Clothes", "Accessories", "Online Shopping", "Grocery Shopping"],
        "Bills": ["Electricity Bill", "Internet Bill", "Water Bill", "Mobile Recharge"],
        "Rent": ["Monthly House Rent"],
        "Entertainment": ["Movie", "Gaming", "Subscription", "Weekend Outing"],
        "Health": ["Medicine", "Doctor Visit", "Health Checkup"],
        "Education": ["Books", "Course Fee", "Stationery", "Exam Fee"],
        "Investment": ["SIP", "Savings Deposit", "Mutual Fund"],
        "Miscellaneous": ["Gift", "Repair", "Unexpected Expense"],
        "Salary": ["Monthly Salary"],
        "Freelance": ["Freelance Payment", "Part-time Work", "Project Payment"],
    }

    records = []

    for date in dates:
        weekday = date.weekday()
        month = date.month

        # Salary once a month
        if date.day == 1:
            amount = np.random.randint(*categories["Salary"])
            records.append({
                "Date": date,
                "Category": "Salary",
                "Description": np.random.choice(descriptions["Salary"]),
                "Amount": amount,
                "Type": "Income",
                "Payment_Method": "Bank Transfer",
            })

        # Freelance sometimes
        if np.random.rand() < 0.08:
            amount = np.random.randint(*categories["Freelance"])
            records.append({
                "Date": date,
                "Category": "Freelance",
                "Description": np.random.choice(descriptions["Freelance"]),
                "Amount": amount,
                "Type": "Income",
                "Payment_Method": "Bank Transfer",
            })

        # Rent once per month
        if date.day == 5:
            amount = np.random.randint(*categories["Rent"])
            records.append({
                "Date": date,
                "Category": "Rent",
                "Description": np.random.choice(descriptions["Rent"]),
                "Amount": amount,
                "Type": "Expense",
                "Payment_Method": "Bank Transfer",
            })

        # Bills a few times per month
        if date.day in [7, 15, 23]:
            amount = np.random.randint(*categories["Bills"])
            records.append({
                "Date": date,
                "Category": "Bills",
                "Description": np.random.choice(descriptions["Bills"]),
                "Amount": amount,
                "Type": "Expense",
                "Payment_Method": np.random.choice(["UPI", "Bank Transfer"]),
            })

        # Daily expenses
        daily_expense_count = np.random.randint(1, 4)
        possible_daily_categories = [
            "Food", "Travel", "Shopping", "Entertainment",
            "Health", "Education", "Investment", "Miscellaneous"
        ]

        for _ in range(daily_expense_count):
            category = np.random.choice(
                possible_daily_categories,
                p=[0.28, 0.18, 0.10, 0.10, 0.07, 0.07, 0.05, 0.15]
            )

            low, high = categories[category]
            amount = np.random.randint(low, high)

            # Weekend behavior
            if weekday in [5, 6] and category in ["Food", "Entertainment", "Shopping"]:
                amount = int(amount * np.random.uniform(1.2, 1.8))

            # Festival / seasonal spike simulation
            if month in [10, 11, 12] and category == "Shopping":
                amount = int(amount * np.random.uniform(1.3, 2.2))

            # Random overspending case
            if np.random.rand() < 0.02:
                amount = int(amount * np.random.uniform(2.0, 4.0))

            records.append({
                "Date": date,
                "Category": category,
                "Description": np.random.choice(descriptions[category]),
                "Amount": amount,
                "Type": "Expense",
                "Payment_Method": np.random.choice(payment_methods),
            })

    df = pd.DataFrame(records)
    df = df.sort_values("Date").reset_index(drop=True)
    df.to_csv(output_path, index=False)
    return df