import pandas as pd

def clean_expense_data(input_path="data/synthetic_expenses.csv",
                       output_path="data/cleaned_expenses.csv"):
    df = pd.read_csv(input_path)

    df = df.drop_duplicates()

    df = df.dropna(subset=["Date", "Category", "Amount", "Type", "Payment_Method"])

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    df["Category"] = df["Category"].astype(str).str.strip().str.title()
    df["Description"] = df["Description"].astype(str).str.strip()
    df["Type"] = df["Type"].astype(str).str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].astype(str).str.strip().str.title()

    df = df.dropna(subset=["Date", "Amount"])
    df = df[df["Amount"] > 0]

    df.to_csv(output_path, index=False)
    return df