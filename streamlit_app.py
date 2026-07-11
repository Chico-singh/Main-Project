import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.title{
    font-size:55px;
    color:#00E5FF;
    font-weight:bold;
}

.subtitle{
    font-size:22px;
    color:white;
}

.feature-card{
    padding:20px;
    border-radius:15px;
    background:#1E1E1E;
    box-shadow:0px 0px 10px #00E5FF;
    text-align:center;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:

    selected = option_menu(
        "FinSight AI",
        [
            "Home",
            "Dashboard",
            "Expense Manager",
            "Income Manager",
            "Analytics",
            "AI Assistant",
            "Forecast",
            "Reports",
            "Settings"
        ],
        icons=[
            "house",
            "bar-chart",
            "wallet2",
            "cash-stack",
            "graph-up",
            "robot",
            "calendar",
            "file-earmark",
            "gear"
        ],
        default_index=0
    )

# ---------- Home ----------
st.markdown(
    "<p class='title'>💎 FinSight AI</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Your Personal AI Financial Assistant</p>",
    unsafe_allow_html=True
)

st.write("")

col1,col2,col3 = st.columns(3)

with col1:
    st.info("💰 Track Income")

with col2:
    st.warning("💸 Manage Expenses")

with col3:
    st.success("🤖 AI Predictions")

st.write("")

st.image(
    "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200",
    use_container_width=True
)

st.markdown("---")

st.header("🚀 Features")

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
<div class="feature-card">
<h3>📊 Dashboard</h3>
Interactive financial dashboard
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="feature-card">
<h3>🤖 AI Assistant</h3>
Expense prediction & recommendations
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="feature-card">
<h3>📈 Analytics</h3>
Beautiful interactive charts
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.success("Developed using Python • Machine Learning • Streamlit • FastAPI")