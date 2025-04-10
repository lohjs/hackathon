import streamlit as st
import pandas as pd
from insight_engine import get_merchant_insights
from chatbot_engine import chatbot_response

# Load cleaned data
data = pd.read_csv("dataset/merged_data.csv")

# Sidebar – Select merchant
merchant_options = (
    data[['merchant_id', 'merchant_name']]
    .drop_duplicates()
    .sort_values('merchant_name')
)

merchant_dict = dict(zip(merchant_options['merchant_name'], merchant_options['merchant_id']))

selected_merchant_name = st.sidebar.selectbox("Select Merchant", list(merchant_dict.keys()))
selected_merchant_id = merchant_dict[selected_merchant_name]

insights = get_merchant_insights(selected_merchant_id, data)

# Header
st.title("📊 Grab Merchant AI Assistant")
st.write(f"🛍️ Insights for: **{selected_merchant_name}**")

# Show KPIs
st.subheader("📈 Business Performance")
st.metric("Total Orders", insights["total_orders"])
st.metric("Total Sales", f"RM{insights['total_sales']:.2f}")
st.metric("Avg Order Value", f"RM{insights['avg_order_value']:.2f}")

# Top items
st.subheader("🍽️ Top Selling Items")
for item, count in insights["top_items"].items():
    st.markdown(f"- **{item}**: {count} orders")

# Alerts
st.subheader("🚨 Alerts & Opportunities")
for alert in insights["alerts"]:
    st.warning(alert)

# Chatbot
st.subheader("🤖 Ask Your AI Assistant")
user_input = st.text_input("Ask a question (e.g., show sales, top items, advice):")

if user_input:
    response = chatbot_response(user_input, selected_merchant_name, insights)
    st.success(response)
