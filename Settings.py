import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Application Settings")

st.markdown("---")

# ---------------- File Paths ----------------

expense_file = "Expenses_Processed.csv"
income_file = "Income_Processed.csv"

# ---------------- Database Status ----------------

st.subheader("📊 Database Status")

expense_rows = 0
income_rows = 0

if os.path.exists(expense_file):
    expense_df = pd.read_csv(expense_file)
    expense_rows = len(expense_df)

if os.path.exists(income_file):
    income_df = pd.read_csv(income_file)
    income_rows = len(income_df)

c1, c2 = st.columns(2)

c1.metric("💸 Expense Records", expense_rows)
c2.metric("💰 Income Records", income_rows)

st.markdown("---")

# ---------------- Delete Expense ----------------

st.subheader("🗑 Expense Data")

if st.button("Delete All Expenses", use_container_width=True):

    columns = [
        "date_time",
        "category",
        "account",
        "amount",
        "currency",
        "tags",
        "description"
    ]

    pd.DataFrame(columns=columns).to_csv(
        expense_file,
        index=False
    )

    st.success("✅ Expense data deleted!")

    st.rerun()

# ---------------- Delete Income ----------------

st.subheader("🗑 Income Data")

if st.button("Delete All Income", use_container_width=True):

    columns = [
        "date_time",
        "category",
        "account",
        "amount",
        "currency",
        "tags",
        "description"
    ]

    pd.DataFrame(columns=columns).to_csv(
        income_file,
        index=False
    )

    st.success("✅ Income data deleted!")

    st.rerun()

# ---------------- Reset Application ----------------

st.markdown("---")

st.subheader("🚨 Reset Entire Application")

if st.button(
    "⚠️ Reset Everything",
    use_container_width=True,
    type="primary"
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

    pd.DataFrame(columns=columns).to_csv(
        expense_file,
        index=False
    )

    pd.DataFrame(columns=columns).to_csv(
        income_file,
        index=False
    )

    st.success("✅ Application Reset Successfully!")

    st.balloons()

    st.rerun()