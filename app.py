import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

sns.set_theme(style="darkgrid")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    color: transparent;
}

.card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(0,255,150,0.4);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

hr {
    border: 1px solid #444;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>📊 PhonePe Transaction Dashboard</div>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## ⚙️ Filters")

state = st.sidebar.selectbox("🌍 Select State", sorted(df['State'].unique()))
year = st.sidebar.selectbox("📅 Select Year", sorted(df['Year'].unique()))

filtered_df = df[(df['State'] == state) & (df['Year'] == year)]

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🏆 Insights"])

# ================= TAB 1 =================
with tab1:
    st.subheader("📌 Key Metrics")

    total_amount = filtered_df['Transaction_Amount'].sum()
    total_txn = filtered_df['Transaction_Count'].sum()
    avg_value = total_amount / total_txn if total_txn != 0 else 0

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'><h4>💰 Total Amount</h4><h2>₹{total_amount:,.0f}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h4>📈 Transactions</h4><h2>{total_txn:,.0f}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h4>💳 Avg Value</h4><h2>₹{avg_value:,.2f}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    # Chart 1
    with col1:
        st.subheader("💳 Transaction by Type")
        type_data = filtered_df.groupby('Transaction_Type')['Transaction_Amount'].sum()

        fig, ax = plt.subplots()
        sns.barplot(x=type_data.index, y=type_data.values, palette="Set2", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Chart 2
    with col2:
        st.subheader("📅 Quarter-wise Transactions")
        quarter_data = filtered_df.groupby('Quarter')['Transaction_Amount'].sum()

        fig, ax = plt.subplots()
        sns.barplot(x=quarter_data.index, y=quarter_data.values, palette="coolwarm", ax=ax)
        st.pyplot(fig)

# ================= TAB 2 =================
with tab2:
    st.subheader("📈 Year-wise Trend")

    year_data = df.groupby('Year')['Transaction_Amount'].sum()

    fig, ax = plt.subplots()
    sns.lineplot(x=year_data.index, y=year_data.values, marker='o', color='cyan', linewidth=3, ax=ax)
    st.pyplot(fig)

# ================= TAB 3 =================
with tab3:
    st.subheader("🏆 Top Insights")

    col1, col2 = st.columns(2)

    # Top States
    with col1:
        st.subheader("Top 10 States")
        top_states = df.groupby('State')['Transaction_Amount'].sum().nlargest(10)

        fig, ax = plt.subplots()
        sns.barplot(x=top_states.values, y=top_states.index, palette="magma", ax=ax)
        st.pyplot(fig)

    # Avg Transaction Count
    with col2:
        st.subheader("📊 Avg Transaction Count")
        avg_count = df.groupby('State')['Transaction_Count'].mean().nlargest(10)

        fig, ax = plt.subplots()
        sns.barplot(x=avg_count.values, y=avg_count.index, palette="cubehelix", ax=ax)
        st.pyplot(fig)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("✨ Built with Streamlit | Premium UI 🚀")