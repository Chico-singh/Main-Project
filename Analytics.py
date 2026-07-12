import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# Load CSS
# --------------------------------------------------

if os.path.exists("assets/styles.css"):
    with open("assets/styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.title("📈 Financial Analytics")

# --------------------------------------------------
# Safe CSV Loader
# --------------------------------------------------

def load_csv(file):

    if os.path.exists(file):

        try:
            return pd.read_csv(file)

        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()

income = load_csv("Income_Processed.csv")
expense = load_csv("Expenses_Processed.csv")

# --------------------------------------------------
# Empty Data Check
# --------------------------------------------------

if income.empty and expense.empty:

    st.info("📂 No financial data found.")

    st.write("Start by adding Income and Expense.")

    st.stop()

# --------------------------------------------------
# Safe Totals
# --------------------------------------------------

if not income.empty and "amount" in income.columns:
    total_income = income["amount"].sum()
else:
    total_income = 0

if not expense.empty and "amount" in expense.columns:
    total_expense = expense["amount"].sum()
else:
    total_expense = 0

savings = total_income - total_expense

if total_income > 0:
    saving_rate = (savings / total_income) * 100
else:
    saving_rate = 0

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("💼 Financial Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Income",
    f"₹ {total_income:,.0f}"
)

c2.metric(
    "💸 Total Expense",
    f"₹ {total_expense:,.0f}"
)

c3.metric(
    "🏦 Savings",
    f"₹ {savings:,.0f}"
)

c4.metric(
    "📈 Saving Rate",
    f"{saving_rate:.1f}%"
)

st.divider()



# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

# Expense Category
if not expense.empty and "category" in expense.columns:

    category = (
        expense.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

else:

    category = pd.DataFrame(
        columns=["category", "amount"]
    )

# Convert Date

if not expense.empty:

    expense["date_time"] = pd.to_datetime(
        expense["date_time"],
        errors="coerce"
    )

    expense["Month"] = expense["date_time"].dt.strftime("%b")

    monthly = (
        expense.groupby("Month")["amount"]
        .sum()
        .reset_index()
    )

else:

    monthly = pd.DataFrame(
        columns=["Month", "amount"]
    )

# --------------------------------------------------
# CHARTS
# --------------------------------------------------

left, right = st.columns(2)

# ==============================
# Expense Distribution
# ==============================

with left:

    st.subheader("🥧 Expense Distribution")

    if category.empty:

        st.info("No expense data available.")

    else:

        fig = px.pie(

            category,

            names="category",

            values="amount",

            hole=0.55,

            color_discrete_sequence=px.colors.qualitative.Set3

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            height=450

        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

# ==============================
# Monthly Trend
# ==============================

with right:

    st.subheader("📈 Monthly Expense Trend")

    if monthly.empty:

        st.info("No monthly data available.")

    else:

        fig2 = px.line(

            monthly,

            x="Month",

            y="amount",

            markers=True

        )

        fig2.update_layout(

            template="plotly_dark",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            height=450

        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

st.divider()

# --------------------------------------------------
# INCOME VS EXPENSE
# --------------------------------------------------

st.subheader("📊 Income vs Expense")

compare = pd.DataFrame({

    "Type": [

        "Income",

        "Expense"

    ],

    "Amount": [

        total_income,

        total_expense

    ]

})

fig3 = px.bar(

    compare,

    x="Type",

    y="Amount",

    color="Type",

    text="Amount"

)

fig3.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    showlegend=False,

    height=450

)

st.plotly_chart(
    fig3,
    width="stretch"
)

st.divider()

# --------------------------------------------------
# TOP SPENDING CATEGORIES
# --------------------------------------------------

st.subheader("🔥 Top Spending Categories")

if category.empty:

    st.info("No categories available.")

else:

    top = category.sort_values(

        by="amount",

        ascending=False

    )

    st.dataframe(

        top,

        width="stretch",

        hide_index=True

    )

st.divider()



# --------------------------------------------------
# AI FINANCIAL INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI Financial Insights")

if expense.empty:

    st.info("No expense data available for AI analysis.")

else:

    top = category.sort_values(
        by="amount",
        ascending=False
    )

    if not top.empty:

        highest = top.iloc[0]

        st.success(
            f"🏆 Highest Spending Category: {highest['category']}"
        )

        st.info(
            f"💸 Total Spent: ₹ {highest['amount']:,.2f}"
        )

    if saving_rate >= 40:

        st.success(
            "🟢 Excellent! Your saving rate is outstanding."
        )

    elif saving_rate >= 20:

        st.warning(
            "🟡 Good! Try increasing your savings a little more."
        )

    elif total_income == 0:

        st.warning(
            "⚠️ Add income to calculate your financial health."
        )

    else:

        st.error(
            "🔴 Your expenses are too high compared to your income."
        )

st.divider()

# --------------------------------------------------
# SMART RECOMMENDATIONS
# --------------------------------------------------

st.subheader("💡 Smart Recommendations")

recommendations = []

if expense.empty:

    recommendations.append(
        "Start tracking your daily expenses."
    )

else:

    if not category.empty:

        highest = category.sort_values(
            by="amount",
            ascending=False
        ).iloc[0]

        if highest["category"] == "Shopping":

            recommendations.append(
                "🛍 Reduce shopping expenses by 10-15%."
            )

        elif highest["category"] == "Food":

            recommendations.append(
                "🍔 Plan meals to reduce food expenses."
            )

        elif highest["category"] == "Travel":

            recommendations.append(
                "✈️ Consider reducing travel expenses."
            )

if total_income == 0:

    recommendations.append(
        "💰 Add your income for better analytics."
    )

elif saving_rate < 20:

    recommendations.append(
        "💵 Try saving at least 20% of your income."
    )

recommendations.append(
    "📈 Review your finances every week."
)

recommendations.append(
    "📊 Analyze your monthly spending habits."
)

for rec in recommendations:

    st.write("✅", rec)

st.divider()

# --------------------------------------------------
# FINANCIAL HEALTH SCORE
# --------------------------------------------------

st.subheader("🏆 Financial Health Score")

if total_income == 0:

    score = 0

elif saving_rate >= 40:

    score = 95

elif saving_rate >= 30:

    score = 85

elif saving_rate >= 20:

    score = 75

elif saving_rate >= 10:

    score = 60

else:

    score = 40

st.progress(score / 100)

st.metric(
    "Overall Score",
    f"{score}/100"
)

if score >= 90:

    st.success("Excellent Financial Health")

elif score >= 75:

    st.info("Good Financial Health")

elif score >= 50:

    st.warning("Average Financial Health")

else:

    st.error("Needs Improvement")

st.divider()

# --------------------------------------------------
# ANALYTICS SUMMARY
# --------------------------------------------------

st.subheader("📋 Analytics Summary")

summary = pd.DataFrame({

    "Metric": [

        "Total Income",

        "Total Expense",

        "Savings",

        "Saving Rate"

    ],

    "Value": [

        f"₹ {total_income:,.2f}",

        f"₹ {total_expense:,.2f}",

        f"₹ {savings:,.2f}",

        f"{saving_rate:.2f}%"

    ]

})

st.dataframe(

    summary,

    width="stretch",

    hide_index=True

)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "💎 FinSight AI | Analytics | Developed by Suryansh Singh"
)