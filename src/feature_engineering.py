import pandas as pd

ESSENTIAL_CATEGORIES = {"Rent", "Bills", "Food", "Health", "Education", "Travel"}

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    df["Month_Num"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.day_name()
    df["Is_Weekend"] = df["Date"].dt.weekday >= 5

    def expense_type(category):
        return "Essential" if category in ESSENTIAL_CATEGORIES else "Non-Essential"

    df["Expense_Nature"] = df["Category"].apply(expense_type)

    def amount_band(amount):
        if amount < 500:
            return "Low"
        elif amount < 3000:
            return "Medium"
        return "High"

    df["Amount_Band"] = df["Amount"].apply(amount_band)
    return df