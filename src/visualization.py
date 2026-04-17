import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def save_category_chart(category_df, path="images/category_expense_chart.png"):
    plt.figure(figsize=(10, 5))
    sns.barplot(data=category_df, x="Category", y="Amount")
    plt.title("Category-wise Expense")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()

def save_monthly_chart(monthly_df, path="images/monthly_income_vs_expense.png"):
    pivot_df = monthly_df.pivot(index="Month_Num", columns="Type", values="Amount").fillna(0)
    plt.figure(figsize=(10, 5))
    for col in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[col], marker="o", label=col)
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month Number")
    plt.ylabel("Amount")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()

def save_payment_chart(payment_df, path="images/payment_method_chart.png"):
    plt.figure(figsize=(8, 5))
    sns.barplot(data=payment_df, x="Payment_Method", y="Amount")
    plt.title("Payment Method Usage")
    plt.xlabel("Payment Method")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()

def save_weekday_chart(weekday_df, path="images/weekday_spending_chart.png"):
    plt.figure(figsize=(10, 5))
    sns.barplot(data=weekday_df, x="Weekday", y="Amount")
    plt.title("Weekday Expense Trend")
    plt.xlabel("Weekday")
    plt.ylabel("Amount")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()

def save_budget_chart(budget_df, path="images/budget_vs_actual_chart.png"):
    plt.figure(figsize=(11, 5))
    budget_df = budget_df.sort_values("Amount", ascending=False)
    x = range(len(budget_df))
    plt.bar(x, budget_df["Amount"], label="Actual")
    plt.bar(x, budget_df["Budget"], alpha=0.6, label="Budget")
    plt.xticks(x, budget_df["Category"], rotation=45)
    plt.title("Budget vs Actual")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()