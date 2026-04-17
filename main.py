import os
from src.data_generator import generate_synthetic_expense_data
from src.data_cleaning import clean_expense_data
from src.feature_engineering import add_features
from src.analysis import (
    category_summary,
    monthly_summary,
    payment_method_summary,
    weekday_summary,
    income_vs_expense_summary,
    weekend_vs_weekday,
    kpis,
    budget_check,
)
from src.insights import generate_insights
from src.visualization import (
    save_category_chart,
    save_monthly_chart,
    save_payment_chart,
    save_weekday_chart,
    save_budget_chart,
)

def ensure_folders():
    folders = ["data", "outputs", "images"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def main():
    ensure_folders()

    print("Step 1: Generating synthetic finance data...")
    raw_df = generate_synthetic_expense_data()

    print("Step 2: Cleaning data...")
    clean_df = clean_expense_data()

    print("Step 3: Adding features...")
    final_df = add_features(clean_df)
    final_df.to_csv("data/final_expense_data.csv", index=False)

    print("Step 4: Running analysis...")
    cat_df = category_summary(final_df)
    mon_df = monthly_summary(final_df)
    pay_df = payment_method_summary(final_df)
    week_df = weekday_summary(final_df)
    income_exp_df = income_vs_expense_summary(final_df)
    weekend_df = weekend_vs_weekday(final_df)
    budget_df = budget_check(final_df)
    kpi_data = kpis(final_df)

    cat_df.to_csv("outputs/category_summary.csv", index=False)
    mon_df.to_csv("outputs/monthly_summary.csv", index=False)
    pay_df.to_csv("outputs/payment_summary.csv", index=False)
    week_df.to_csv("outputs/weekday_summary.csv", index=False)
    income_exp_df.to_csv("outputs/income_vs_expense_summary.csv", index=False)
    weekend_df.to_csv("outputs/weekend_vs_weekday_summary.csv", index=False)
    budget_df.to_csv("outputs/budget_check.csv", index=False)

    print("Step 5: Saving charts...")
    save_category_chart(cat_df)
    save_monthly_chart(mon_df)
    save_payment_chart(pay_df)
    save_weekday_chart(week_df)
    save_budget_chart(budget_df)

    print("Step 6: Generating insights...")
    insights = generate_insights(final_df, kpi_data, cat_df, budget_df, weekend_df)

    with open("outputs/insights.txt", "w", encoding="utf-8") as f:
        for i, insight in enumerate(insights, start=1):
            f.write(f"{i}. {insight}\n")

    print("\nProject Execution Complete")
    print(f"Total Income: ₹{kpi_data['total_income']:,.0f}")
    print(f"Total Expense: ₹{kpi_data['total_expense']:,.0f}")
    print(f"Balance: ₹{kpi_data['balance']:,.0f}")
    print(f"Highest Spending Category: {kpi_data['highest_category']}")
    print(f"Total Transactions: {kpi_data['transactions']}")

    print("\nInsights:")
    for insight in insights:
        print(f"- {insight}")

if __name__ == "__main__":
    main()