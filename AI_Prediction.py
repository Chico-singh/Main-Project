import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Prediction",
    page_icon="🤖",
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

st.title("🤖 AI Financial Prediction")

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

total_income = income["amount"].sum() if not income.empty and "amount" in income.columns else 0

total_expense = expense["amount"].sum() if not expense.empty and "amount" in expense.columns else 0

savings = total_income - total_expense

saving_rate = (savings / total_income * 100) if total_income > 0 else 0

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("📊 Financial Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Income", f"₹ {total_income:,.0f}")

c2.metric("💸 Expense", f"₹ {total_expense:,.0f}")

c3.metric("🏦 Savings", f"₹ {savings:,.0f}")

c4.metric("📈 Saving Rate", f"{saving_rate:.1f}%")

st.divider()






# --------------------------------------------------
# AI SPENDING ANALYSIS
# --------------------------------------------------

st.subheader("🧠 AI Spending Analysis")

if expense.empty:

    st.info("No expense data available.")

else:

    category = (
        expense.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    top = category.sort_values(
        by="amount",
        ascending=False
    )

    highest = top.iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"🏆 Highest Spending Category\n\n"
            f"**{highest['category']}**"
        )

        st.metric(
            "Amount",
            f"₹ {highest['amount']:,.0f}"
        )

    with col2:

        fig = px.pie(

            category,

            names="category",

            values="amount",

            hole=0.6,

            color_discrete_sequence=px.colors.qualitative.Set3

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            height=420

        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

st.divider()

# --------------------------------------------------
# AI BUDGET SCORE
# --------------------------------------------------

st.subheader("🏆 AI Budget Score")

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
    "Budget Score",
    f"{score}/100"
)

st.divider()

# --------------------------------------------------
# NEXT MONTH PREDICTION
# --------------------------------------------------

st.subheader("🔮 AI Prediction")

predicted_expense = total_expense * 1.05

predicted_income = total_income

predicted_saving = predicted_income - predicted_expense

c1, c2, c3 = st.columns(3)

c1.metric(
    "Predicted Income",
    f"₹ {predicted_income:,.0f}"
)

c2.metric(
    "Predicted Expense",
    f"₹ {predicted_expense:,.0f}"
)

c3.metric(
    "Predicted Saving",
    f"₹ {predicted_saving:,.0f}"
)

st.divider()

# --------------------------------------------------
# AI INSIGHT
# --------------------------------------------------

st.subheader("🤖 AI Insight")

if predicted_saving > 0:

    st.success(
        f"""
        Based on your current spending,
        you are expected to save

        ₹ {predicted_saving:,.0f}

        next month.
        """
    )

else:

    st.error(
        f"""
        AI predicts you may overspend by

        ₹ {abs(predicted_saving):,.0f}

        next month.
        """
    )

st.divider()

# --------------------------------------------------
# SMART FINANCIAL RECOMMENDATIONS
# --------------------------------------------------

st.subheader("💡 Smart Financial Recommendations")

recommendations = []

if total_income == 0:
    recommendations.append("💰 Add your income to enable AI analysis.")

if expense.empty:
    recommendations.append("📝 Add some expenses to receive personalized suggestions.")

if total_income > 0 and saving_rate < 20:
    recommendations.append("💵 Try saving at least 20% of your income every month.")

if total_expense > total_income and total_income > 0:
    recommendations.append("⚠ Your expenses are higher than your income.")

if not expense.empty:

    category = (
        expense.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    if not category.empty:

        highest = category.sort_values(
            by="amount",
            ascending=False
        ).iloc[0]

        if highest["category"] == "Shopping":
            recommendations.append(
                "🛍 Shopping is your highest expense. Consider setting a monthly shopping budget."
            )

        elif highest["category"] == "Food":
            recommendations.append(
                "🍔 Meal planning could help reduce food expenses."
            )

        elif highest["category"] == "Travel":
            recommendations.append(
                "✈ Review travel expenses and look for cost-saving options."
            )

recommendations.append("📊 Review your finances every week.")
recommendations.append("📈 Track your monthly spending trends.")

for rec in recommendations:
    st.write("✅", rec)

st.divider()

# --------------------------------------------------
# FINANCIAL HEALTH
# --------------------------------------------------

st.subheader("❤️ Financial Health")

if score >= 90:

    st.success("Excellent Financial Health")

elif score >= 75:

    st.info("Good Financial Health")

elif score >= 50:

    st.warning("Average Financial Health")

else:

    st.error("Needs Improvement")

st.progress(score / 100)

st.divider()

# --------------------------------------------------
# PREDICTION SUMMARY
# --------------------------------------------------

st.subheader("📋 Prediction Summary")

summary = pd.DataFrame({

    "Metric": [

        "Current Income",

        "Current Expense",

        "Current Savings",

        "Saving Rate",

        "Predicted Next Month Expense",

        "Predicted Next Month Savings"

    ],

    "Value": [

        f"₹ {total_income:,.2f}",

        f"₹ {total_expense:,.2f}",

        f"₹ {savings:,.2f}",

        f"{saving_rate:.2f}%",

        f"₹ {predicted_expense:,.2f}",

        f"₹ {predicted_saving:,.2f}"

    ]

})

st.dataframe(

    summary,

    width="stretch",

    hide_index=True

)

st.divider()

# --------------------------------------------------
# AI STATUS
# --------------------------------------------------

st.subheader("🤖 AI Status")

if predicted_saving > 0:

    st.success(
        "AI Prediction: Your finances are on a healthy track."
    )

else:

    st.error(
        "AI Prediction: You may overspend next month. Consider reducing discretionary expenses."
    )

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "💎 FinSight AI | AI Prediction | Developed by Suryansh Singh"
)