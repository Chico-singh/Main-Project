import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
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

st.title("📄 Financial Reports")

# --------------------------------------------------
# Safe CSV Loader
# --------------------------------------------------

def load_csv(file):

    if os.path.exists(file):

        try:
            return pd.read_csv(file)

        except:
            return pd.DataFrame()

    return pd.DataFrame()

income = load_csv("Income_Processed.csv")
expense = load_csv("Expenses_Processed.csv")

# --------------------------------------------------
# Empty Check
# --------------------------------------------------

if income.empty and expense.empty:

    st.info("📂 No financial data found.")

    st.write("Please add Income and Expense first.")

    st.stop()

# --------------------------------------------------
# Safe Totals
# --------------------------------------------------

total_income = (
    income["amount"].sum()
    if not income.empty and "amount" in income.columns
    else 0
)

total_expense = (
    expense["amount"].sum()
    if not expense.empty and "amount" in expense.columns
    else 0
)

savings = total_income - total_expense

saving_rate = (
    (savings / total_income) * 100
    if total_income > 0
    else 0
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("📊 Report Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Income",
    f"₹ {total_income:,.0f}"
)

c2.metric(
    "💸 Expense",
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

# Income vs Expense
compare = pd.DataFrame({
    "Type": ["Income", "Expense"],
    "Amount": [total_income, total_expense]
})

# Expense by Category
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

# Monthly Expense

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

# ===============================
# Income vs Expense Pie Chart
# ===============================

with left:

    st.subheader("🥧 Income vs Expense")

    fig1 = px.pie(

        compare,

        names="Type",

        values="Amount",

        hole=0.55,

        color_discrete_sequence=["#4CAF50", "#F44336"]

    )

    fig1.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        height=420

    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

# ===============================
# Expense Category
# ===============================

with right:

    st.subheader("📊 Expense Categories")

    if category.empty:

        st.info("No expense data available.")

    else:

        fig2 = px.bar(

            category,

            x="category",

            y="amount",

            color="category",

            text="amount"

        )

        fig2.update_layout(

            template="plotly_dark",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            showlegend=False,

            height=420

        )

        st.plotly_chart(
            fig2,
            width="stretch"
        )

st.divider()

# --------------------------------------------------
# MONTHLY EXPENSE REPORT
# --------------------------------------------------

st.subheader("📈 Monthly Expense Report")

if monthly.empty:

    st.info("No monthly data available.")

else:

    fig3 = px.line(

        monthly,

        x="Month",

        y="amount",

        markers=True

    )

    fig3.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

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

    st.info("No category data available.")

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
# RECENT TRANSACTIONS
# --------------------------------------------------

st.subheader("📋 Recent Transactions")

tab1, tab2 = st.tabs(["💰 Income", "💸 Expense"])

with tab1:

    if income.empty:

        st.info("No income records found.")

    else:

        income_show = income.copy()

        if "date_time" in income_show.columns:

            income_show = income_show.sort_values(
                by="date_time",
                ascending=False
            )

        st.dataframe(
            income_show,
            width="stretch",
            hide_index=True
        )

with tab2:

    if expense.empty:

        st.info("No expense records found.")

    else:

        expense_show = expense.copy()

        if "date_time" in expense_show.columns:

            expense_show = expense_show.sort_values(
                by="date_time",
                ascending=False
            )

        st.dataframe(
            expense_show,
            width="stretch",
            hide_index=True
        )

st.divider()

# --------------------------------------------------
# DOWNLOAD REPORTS
# --------------------------------------------------

st.subheader("📥 Download Reports")

c1, c2 = st.columns(2)

with c1:

    if not income.empty:

        csv = income.to_csv(index=False).encode("utf-8")

        st.download_button(

            "⬇ Download Income CSV",

            data=csv,

            file_name="Income_Report.csv",

            mime="text/csv",

            width="stretch"

        )

with c2:

    if not expense.empty:

        csv = expense.to_csv(index=False).encode("utf-8")

        st.download_button(

            "⬇ Download Expense CSV",

            data=csv,

            file_name="Expense_Report.csv",

            mime="text/csv",

            width="stretch"

        )

st.divider()

# --------------------------------------------------
# AI REPORT SUMMARY
# --------------------------------------------------

st.subheader("🤖 AI Report Summary")

if total_income == 0:

    st.warning(
        "Please add income data to generate AI insights."
    )

else:

    if saving_rate >= 40:

        st.success(
            "Excellent! Your financial performance is outstanding."
        )

    elif saving_rate >= 20:

        st.info(
            "Good financial performance. Keep improving your savings."
        )

    else:

        st.error(
            "Your expenses are reducing your savings significantly."
        )

st.divider()

# --------------------------------------------------
# REPORT CARD
# --------------------------------------------------

st.subheader("🏆 Financial Report Card")

if saving_rate >= 40:

    grade = "A+"

elif saving_rate >= 30:

    grade = "A"

elif saving_rate >= 20:

    grade = "B"

elif saving_rate >= 10:

    grade = "C"

else:

    grade = "D"

c1, c2 = st.columns(2)

c1.metric(
    "Financial Grade",
    grade
)

c2.metric(
    "Saving Rate",
    f"{saving_rate:.1f}%"
)

st.progress(min(max(saving_rate / 100, 0), 1))

st.divider()

# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

st.subheader("📑 Final Summary")

summary = pd.DataFrame({

    "Metric": [

        "Total Income",

        "Total Expense",

        "Savings",

        "Saving Rate",

        "Financial Grade"

    ],

    "Value": [

        f"₹ {total_income:,.2f}",

        f"₹ {total_expense:,.2f}",

        f"₹ {savings:,.2f}",

        f"{saving_rate:.2f}%",

        grade

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
    "💎 FinSight AI | Reports | Developed by Suryansh Singh"
)