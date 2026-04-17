def generate_insights(df, kpi_data, category_df, budget_df, weekend_df):
    insights = []

    insights.append(
        f"Total income is ₹{kpi_data['total_income']:,.0f} and total expense is ₹{kpi_data['total_expense']:,.0f}."
    )

    insights.append(
        f"Current balance is ₹{kpi_data['balance']:,.0f}."
    )

    if not category_df.empty:
        top_cat = category_df.iloc[0]
        insights.append(
            f"Highest spending category is {top_cat['Category']} with ₹{top_cat['Amount']:,.0f}."
        )

    if not budget_df.empty:
        overspent = budget_df[budget_df["Over_Budget"]]
        if not overspent.empty:
            categories = ", ".join(overspent["Category"].tolist())
            insights.append(f"Overspending detected in these categories: {categories}.")
        else:
            insights.append("No category has crossed its defined budget.")

    if len(weekend_df) == 2:
        weekend_amt = weekend_df.loc[weekend_df["Day_Type"] == "Weekend", "Amount"]
        weekday_amt = weekend_df.loc[weekend_df["Day_Type"] == "Weekday", "Amount"]

        if not weekend_amt.empty and not weekday_amt.empty:
            if weekend_amt.iloc[0] > weekday_amt.iloc[0]:
                insights.append("Weekend spending is higher than weekday spending.")
            else:
                insights.append("Weekday spending is higher than weekend spending.")

    if kpi_data["balance"] < 0:
        insights.append("Expenses are higher than income. Budget correction is needed.")
    else:
        insights.append("Income is higher than expenses, which indicates a positive financial position.")

    return insights