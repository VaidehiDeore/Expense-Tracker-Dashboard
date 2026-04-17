import os
import sys
from pathlib import Path

# Prevent OpenBLAS memory/thread issues
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.analysis import (
    category_summary,
    monthly_summary,
    payment_method_summary,
    weekday_summary,
    weekend_vs_weekday,
    kpis,
    budget_check,
)
from src.insights import generate_insights


# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #eef2ff 0%, #dfe6ff 45%, #edf1ff 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7f9ff 0%, #e8edff 100%);
        border-right: 1px solid rgba(112, 128, 220, 0.18);
    }

    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 1.5rem;
        max-width: 1450px;
    }

    .hero-box {
        background: rgba(255,255,255,0.74);
        border: 1px solid rgba(255,255,255,0.70);
        border-radius: 28px;
        padding: 22px 26px;
        box-shadow: 0 16px 36px rgba(83, 100, 202, 0.12);
        backdrop-filter: blur(10px);
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        color: #3346b5;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 15px;
        color: #6b78a8;
        margin-bottom: 14px;
    }

    .pill {
        display: inline-block;
        background: linear-gradient(135deg, #6a6cff, #904dff);
        color: white;
        font-size: 12px;
        font-weight: 700;
        padding: 8px 14px;
        border-radius: 999px;
        margin-right: 8px;
        margin-bottom: 8px;
        box-shadow: 0 8px 18px rgba(96, 83, 240, 0.22);
    }

    .kpi-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.82), rgba(245,247,255,0.74));
        border: 1px solid rgba(255,255,255,0.72);
        border-radius: 24px;
        padding: 18px 20px;
        box-shadow: 0 12px 28px rgba(76, 92, 190, 0.12);
        backdrop-filter: blur(10px);
        min-height: 110px;
        transition: all 0.25s ease;
    }

    .kpi-box:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 18px 36px rgba(76, 92, 190, 0.18);
    }

    .kpi-label {
        font-size: 14px;
        font-weight: 700;
        color: #6c78a8;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #5a3ef0;
        line-height: 1.15;
    }

    .kpi-sub {
        font-size: 12px;
        color: #8c96bf;
        margin-top: 8px;
    }

    .section-card {
        background: rgba(255,255,255,0.76);
        border: 1px solid rgba(255,255,255,0.68);
        border-radius: 24px;
        padding: 10px 12px 6px 12px;
        box-shadow: 0 14px 30px rgba(74, 92, 187, 0.10);
        backdrop-filter: blur(10px);
        margin-bottom: 16px;
        transition: transform 0.3s ease;
    }

    .section-card:hover {
        transform: translateY(-4px);
    }

    .section-title {
        font-size: 20px;
        font-weight: 800;
        color: #3645ac;
        margin-bottom: 10px;
    }

    .insight {
        background: rgba(247,249,255,0.98);
        border-left: 5px solid #6d63ff;
        padding: 12px 14px;
        border-radius: 14px;
        margin-bottom: 10px;
        color: #44527f;
        font-size: 14px;
        line-height: 1.7;
    }

    .balance-chip {
        background: linear-gradient(135deg, #6d70ff 0%, #8857ff 100%);
        color: white;
        border-radius: 22px;
        padding: 16px 18px;
        box-shadow: 0 14px 28px rgba(98, 83, 240, 0.22);
        margin-top: 6px;
    }

    .balance-chip-label {
        font-size: 13px;
        opacity: 0.92;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .balance-chip-value {
        font-size: 26px;
        font-weight: 800;
        line-height: 1.1;
    }

    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] {
        background-color: #ff5c5c !important;
        color: white !important;
        border-radius: 8px !important;
    }

    .dataframe {
        border-radius: 14px !important;
        overflow: hidden !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- DATA ----------------
data_path = ROOT / "data" / "final_expense_data.csv"

if not data_path.exists():
    st.error("Run main.py first so the file data/final_expense_data.csv gets created.")
    st.stop()

df = pd.read_csv(data_path)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"]).copy()

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

if "Month" not in df.columns:
    df["Month"] = df["Date"].dt.month_name()

ordered_months = [m for m in month_order if m in df["Month"].unique()]

# ---------------- SIDEBAR ----------------
st.sidebar.markdown(
    """
    ### 💼 Personal Finance
    <small style="color:#6b78a8;">Premium finance dashboard</small>
    """,
    unsafe_allow_html=True,
)

selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=sorted(df["Category"].dropna().unique().tolist()),
    default=sorted(df["Category"].dropna().unique().tolist()),
)

selected_type = st.sidebar.selectbox(
    "Transaction type",
    ["All", "Expense", "Income"],
)

selected_months = st.sidebar.multiselect(
    "Select months",
    options=ordered_months,
    default=ordered_months,
)

show_raw = st.sidebar.checkbox("Show raw filtered data", value=False)

filtered_df = df.copy()

if selected_categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]

if selected_months:
    filtered_df = filtered_df[filtered_df["Month"].isin(selected_months)]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["Type"] == selected_type]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------------- ANALYSIS ----------------
kpi_data = kpis(filtered_df)
cat_df = category_summary(filtered_df)
mon_df = monthly_summary(filtered_df)
pay_df = payment_method_summary(filtered_df)
week_df = weekday_summary(filtered_df)
weekend_df = weekend_vs_weekday(filtered_df)
budget_df = budget_check(filtered_df)
insights = generate_insights(filtered_df, kpi_data, cat_df, budget_df, weekend_df)


def fmt_inr(x):
    return f"₹{x:,.0f}"


# ---------------- CHART HELPERS ----------------
def make_bar_chart(data, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(7, 4))
    palette = ["#6C63FF", "#8476FF", "#9A8BFF", "#B0A2FF", "#C7BBFF"]
    colors = [palette[i % len(palette)] for i in range(len(data))]

    bars = ax.bar(data[x_col], data[y_col], color=colors, edgecolor="none", alpha=0.95)

    ax.set_title(title, fontsize=16, fontweight="bold", color="#3741a0")
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.2)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height/1000)}K",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#4a4a4a",
        )

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    fig.patch.set_alpha(0)
    return fig


def make_line_chart(monthly_pivot):
    fig, ax = plt.subplots(figsize=(7, 4))

    if "Expense" in monthly_pivot.columns:
        ax.plot(
            monthly_pivot.index,
            monthly_pivot["Expense"],
            marker="o",
            linewidth=3,
            label="Expense",
            color="#ff4d6d",
        )
        ax.fill_between(
            monthly_pivot.index,
            monthly_pivot["Expense"],
            alpha=0.08,
            color="#ff4d6d",
        )

    if "Income" in monthly_pivot.columns:
        ax.plot(
            monthly_pivot.index,
            monthly_pivot["Income"],
            marker="o",
            linewidth=3,
            label="Income",
            color="#4CAF50",
        )

    ax.set_title("Monthly Income vs Expense", fontsize=16, fontweight="bold", color="#3741a0")
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.2)
    ax.legend()

    plt.tight_layout()
    fig.patch.set_alpha(0)
    return fig


# ---------------- HERO ----------------
pill_html = "".join(
    [f'<span class="pill">{m[:3].upper()}</span>' for m in selected_months[:6]]
)

st.markdown(
    f"""
    <div class="hero-box">
        <div class="hero-title">💰 Expense Tracker Dashboard</div>
        <div class="hero-subtitle">
            Modern personal finance analytics system with income, expenses, trends, budgeting, and actionable insights
        </div>
        {pill_html}
        <span class="pill">Analytics</span>
        <span class="pill">Premium UI</span>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([3, 1])
with hero_right:
    st.markdown(
        f"""
        <div class="balance-chip">
            <div class="balance-chip-label">Current Balance</div>
            <div class="balance-chip-value">{fmt_inr(kpi_data["balance"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- KPI ----------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-label">Total Income</div>
            <div class="kpi-value">💰 {fmt_inr(kpi_data["total_income"])}</div>
            <div class="kpi-sub">All selected transactions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-label">Total Expense</div>
            <div class="kpi-value">💸 {fmt_inr(kpi_data["total_expense"])}</div>
            <div class="kpi-sub">Tracked expense amount</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    balance_color = "#1db954" if kpi_data["balance"] >= 0 else "#ff4d4d"
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-label">Balance</div>
            <div class="kpi-value" style="color:{balance_color};">📊 {fmt_inr(kpi_data["balance"])}</div>
            <div class="kpi-sub">Income minus expense</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-label">Top Category</div>
            <div class="kpi-value">🏆 {kpi_data["highest_category"]}</div>
            <div class="kpi-sub">Highest spending category</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------------- ROW 1 ----------------
c1, c2 = st.columns([1.55, 1])

with c1:
    st.markdown('<div class="section-title">Category-wise Expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if not cat_df.empty:
        fig = make_bar_chart(cat_df, "Category", "Amount", "Category-wise Expense")
        st.pyplot(fig)
    else:
        st.info("No category data available.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-title">Payment Method Usage</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if not pay_df.empty:
        fig = make_bar_chart(pay_df, "Payment_Method", "Amount", "Payment Method Usage")
        st.pyplot(fig)
    else:
        st.info("No payment method data available.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- ROW 2 ----------------
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="section-title">Monthly Income vs Expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if not mon_df.empty:
        monthly_pivot = mon_df.pivot(index="Month_Num", columns="Type", values="Amount").fillna(0)
        fig = make_line_chart(monthly_pivot)
        st.pyplot(fig)
    else:
        st.info("No monthly summary available.")
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown('<div class="section-title">Weekday Spending</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if not week_df.empty:
        fig = make_bar_chart(week_df, "Weekday", "Amount", "Weekday Spending")
        st.pyplot(fig)
    else:
        st.info("No weekday data available.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- ROW 3 ----------------
c5, c6 = st.columns([1.1, 1])

with c5:
    st.markdown('<div class="section-title">Budget vs Actual</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if not budget_df.empty:
        budget_show = budget_df[["Category", "Amount", "Budget", "Difference", "Over_Budget"]].copy()
        budget_show["Amount"] = budget_show["Amount"].map(fmt_inr)
        budget_show["Budget"] = budget_show["Budget"].map(lambda x: fmt_inr(x) if pd.notnull(x) else "N/A")
        budget_show["Difference"] = budget_show["Difference"].map(lambda x: fmt_inr(x) if pd.notnull(x) else "N/A")
        budget_show["Status"] = budget_show["Over_Budget"].map({True: "Over Budget", False: "Within Budget"})
        budget_show = budget_show.drop(columns=["Over_Budget"])
        st.dataframe(budget_show, use_container_width=True, height=320)
    else:
        st.info("No budget data available.")
    st.markdown("</div>", unsafe_allow_html=True)

with c6:
    st.markdown('<div class="section-title">Financial Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if insights:
        for item in insights:
            st.markdown(
                f"""
                <div class="insight">💡 {item}</div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No insights available.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RAW DATA ----------------
if show_raw:
    st.markdown("---")
    st.markdown('<div class="section-title">Filtered Transactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df.sort_values("Date", ascending=False).head(50),
        use_container_width=True,
        height=360,
    )
    st.markdown("</div>", unsafe_allow_html=True)