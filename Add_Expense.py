import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="Add Expense",
    page_icon="💸",
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

st.title("💸 Add Expense")

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

expense = load_csv("Expenses_Processed.csv")

# --------------------------------------------------
# Expense Form
# --------------------------------------------------

st.subheader("➕ New Expense")

col1, col2 = st.columns(2)

with col1:

    date = st.date_input(
        "📅 Date",
        datetime.today()
    )

    category = st.selectbox(
        "🛍 Category",
        [
            "Food",
            "Shopping",
            "Transport",
            "Entertainment",
            "Bills",
            "Healthcare",
            "Education",
            "Travel",
            "Other"
        ]
    )

    amount = st.number_input(
        "💰 Amount",
        min_value=0.0,
        step=10.0,
        format="%.2f"
    )

with col2:

    account = st.selectbox(
        "💳 Payment Method",
        [
            "Cash",
            "UPI",
            "Bank",
            "Credit Card",
            "Debit Card"
        ]
    )

    currency = st.selectbox(
        "💱 Currency",
        [
            "INR",
            "USD",
            "EUR"
        ]
    )

    tags = st.text_input(
        "🏷 Tags"
    )

description = st.text_area(
    "📝 Description"
)


# --------------------------------------------------
# SAVE EXPENSE
# --------------------------------------------------

st.markdown("---")

if st.button("💾 Save Expense", width="stretch"):

    if amount <= 0:

        st.error("Please enter a valid amount.")

    else:

        new_data = pd.DataFrame([{

            "date_time": str(date),

            "category": category,

            "account": account,

            "amount": amount,

            "currency": currency,

            "tags": tags,

            "description": description

        }])

        file = "Expenses_Processed.csv"

        if os.path.exists(file):

            try:

                df = pd.read_csv(file)

                df = pd.concat(
                    [df, new_data],
                    ignore_index=True
                )

            except:

                df = new_data

        else:

            df = new_data

        df.to_csv(file, index=False)

        st.success("✅ Expense Saved Successfully!")

        st.balloons()

        st.rerun()

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

expense = load_csv("Expenses_Processed.csv")

st.markdown("---")

st.subheader("📊 Expense Summary")

if expense.empty:

    st.info("No expense records available.")

else:

    expense["date_time"] = pd.to_datetime(
        expense["date_time"],
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    today_expense = expense[
        expense["date_time"].dt.normalize() == today
    ]["amount"].sum()

    month_expense = expense[
        expense["date_time"].dt.month ==
        datetime.today().month
    ]["amount"].sum()

    total_expense = expense["amount"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📅 Today",
        f"₹ {today_expense:,.0f}"
    )

    c2.metric(
        "📆 This Month",
        f"₹ {month_expense:,.0f}"
    )

    c3.metric(
        "💸 Total Expense",
        f"₹ {total_expense:,.0f}"
    )

# --------------------------------------------------
# RECENT EXPENSES
# --------------------------------------------------

st.markdown("---")

st.subheader("📋 Recent Expenses")

if expense.empty:

    st.info("No expenses found.")

else:

    recent = expense.sort_values(
        by="date_time",
        ascending=False
    )

    st.dataframe(
        recent,
        width="stretch",
        hide_index=True
    )

st.divider()



# --------------------------------------------------
# DELETE SELECTED EXPENSE
# --------------------------------------------------

if not expense.empty:

    st.markdown("---")
    st.subheader("🗑 Delete Expense")

    # Create a readable transaction list
    expense["Display"] = (
        expense["date_time"].astype(str)
        + " | "
        + expense["category"].astype(str)
        + " | ₹"
        + expense["amount"].astype(str)
    )

    selected = st.selectbox(
        "Select Expense",
        expense["Display"]
    )

    if st.button(
        "🗑 Delete Selected Expense",
        width="stretch"
    ):

        expense = expense[
            expense["Display"] != selected
        ]

        expense = expense.drop(
            columns=["Display"],
            errors="ignore"
        )

        expense.to_csv(
            "Expenses_Processed.csv",
            index=False
        )

        st.success("✅ Expense Deleted Successfully!")

        st.rerun()

# --------------------------------------------------
# DELETE ALL EXPENSES
# --------------------------------------------------

st.markdown("---")

st.subheader("⚠️ Reset Expense Data")

if st.button(
    "🗑 Delete All Expenses",
    type="primary",
    width="stretch"
):

    columns = [
        "date_time",
        "category",
        "account",
        "amount",
        "currency",
        "tags",
        "description"
    ]

    empty_df = pd.DataFrame(columns=columns)

    empty_df.to_csv(
        "Expenses_Processed.csv",
        index=False
    )

    st.success("✅ All Expenses Deleted!")

    st.balloons()

    st.rerun()

# --------------------------------------------------
# PAGE FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "💎 FinSight AI | Expense Manager | Developed by Suryansh Singh"
)