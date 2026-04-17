import pandas as pd

def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[df["Type"] == "Expense"]
        .groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["Month_Num", "Month", "Type"], as_index=False)["Amount"]
        .sum()
        .sort_values(["Month_Num", "Type"])
    )

def payment_method_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Payment_Method", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

def weekday_summary(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    result = (
        df[df["Type"] == "Expense"]
        .groupby("Weekday", as_index=False)["Amount"]
        .sum()
    )
    result["Weekday"] = pd.Categorical(result["Weekday"], categories=order, ordered=True)
    return result.sort_values("Weekday")

def income_vs_expense_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Type", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

def weekend_vs_weekday(df: pd.DataFrame) -> pd.DataFrame:
    temp = df[df["Type"] == "Expense"].copy()
    temp["Day_Type"] = temp["Is_Weekend"].map({True: "Weekend", False: "Weekday"})
    return temp.groupby("Day_Type", as_index=False)["Amount"].sum()

def kpis(df: pd.DataFrame) -> dict:
    total_income = df.loc[df["Type"] == "Income", "Amount"].sum()
    total_expense = df.loc[df["Type"] == "Expense", "Amount"].sum()
    balance = total_income - total_expense

    expense_df = df[df["Type"] == "Expense"]
    highest_category = (
        expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).index[0]
        if not expense_df.empty else "N/A"
    )

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "balance": float(balance),
        "highest_category": highest_category,
        "transactions": int(len(df)),
    }

def budget_check(df: pd.DataFrame) -> pd.DataFrame:
    budgets = {
        "Food": 12000,
        "Travel": 6000,
        "Shopping": 15000,
        "Bills": 10000,
        "Rent": 150000,
        "Entertainment": 10000,
        "Health": 12000,
        "Education": 20000,
        "Investment": 50000,
        "Miscellaneous": 10000,
    }

    expense_totals = (
        df[df["Type"] == "Expense"]
        .groupby("Category", as_index=False)["Amount"]
        .sum()
    )

    expense_totals["Budget"] = expense_totals["Category"].map(budgets)
    expense_totals["Over_Budget"] = expense_totals["Amount"] > expense_totals["Budget"]
    expense_totals["Difference"] = expense_totals["Amount"] - expense_totals["Budget"]
    return expense_totals.sort_values("Amount", ascending=False)