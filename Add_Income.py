import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Add Income",
    page_icon="💰",
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

st.title("💰 Add Income")

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

# --------------------------------------------------
# Income Form
# --------------------------------------------------

st.subheader("➕ New Income")

col1, col2 = st.columns(2)

with col1:

    date = st.date_input(
        "📅 Date",
        datetime.today()
    )

    category = st.selectbox(
        "💼 Income Source",
        [
            "Salary",
            "Business",
            "Freelancing",
            "Investment",
            "Bonus",
            "Gift",
            "Rental",
            "Other"
        ]
    )

    amount = st.number_input(
        "💰 Amount",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )

with col2:

    account = st.selectbox(
        "🏦 Deposit Account",
        [
            "Bank",
            "Cash",
            "UPI",
            "Wallet"
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
        "🏷 Reference"
    )

description = st.text_area(
    "📝 Description"
)





# --------------------------------------------------
# SAVE INCOME
# --------------------------------------------------

st.markdown("---")

if st.button("💾 Save Income", width="stretch"):

    if amount <= 0:

        st.error("⚠ Please enter a valid amount.")

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

        file = "Income_Processed.csv"

        if os.path.exists(file):

            try:

                df = pd.read_csv(file)

                df = pd.concat(
                    [df, new_data],
                    ignore_index=True
                )

            except Exception:

                df = new_data

        else:

            df = new_data

        df.to_csv(file, index=False)

        st.success("✅ Income Saved Successfully!")

        st.balloons()

        st.rerun()

# --------------------------------------------------
# LOAD UPDATED DATA
# --------------------------------------------------

income = load_csv("Income_Processed.csv")

# --------------------------------------------------
# INCOME SUMMARY
# --------------------------------------------------

st.markdown("---")

st.subheader("📊 Income Summary")

if income.empty:

    st.info("No income records available.")

else:

    income["date_time"] = pd.to_datetime(
        income["date_time"],
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    today_income = income[
        income["date_time"].dt.normalize() == today
    ]["amount"].sum()

    month_income = income[
        income["date_time"].dt.month ==
        datetime.today().month
    ]["amount"].sum()

    total_income = income["amount"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📅 Today",
        f"₹ {today_income:,.0f}"
    )

    c2.metric(
        "📆 This Month",
        f"₹ {month_income:,.0f}"
    )

    c3.metric(
        "💰 Total Income",
        f"₹ {total_income:,.0f}"
    )

# --------------------------------------------------
# RECENT INCOME
# --------------------------------------------------

st.markdown("---")

st.subheader("📋 Recent Income")

if income.empty:

    st.info("No income records found.")

else:

    recent = income.sort_values(
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
# DELETE SELECTED INCOME
# --------------------------------------------------

if not income.empty:

    st.markdown("---")
    st.subheader("🗑 Delete Income")

    # Create a readable transaction list
    income["Display"] = (
        income["date_time"].astype(str)
        + " | "
        + income["category"].astype(str)
        + " | ₹"
        + income["amount"].astype(str)
    )

    selected = st.selectbox(
        "Select Income",
        income["Display"]
    )

    if st.button(
        "🗑 Delete Selected Income",
        width="stretch"
    ):

        # Delete only the selected transaction
        row_index = income[income["Display"] == selected].index[0]

        income = income.drop(row_index)

        income = income.drop(
            columns=["Display"],
            errors="ignore"
        )

        income.to_csv(
            "Income_Processed.csv",
            index=False
        )

        st.success("✅ Income Deleted Successfully!")

        st.balloons()

        st.rerun()

# --------------------------------------------------
# DELETE ALL INCOME
# --------------------------------------------------

st.markdown("---")

st.subheader("⚠️ Reset Income Data")

if st.button(
    "🗑 Delete All Income",
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
        "Income_Processed.csv",
        index=False
    )

    st.success("✅ All Income Deleted Successfully!")

    st.balloons()

    st.rerun()

# --------------------------------------------------
# PAGE FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "💎 FinSight AI | Income Manager | Developed by Suryansh Singh"
)