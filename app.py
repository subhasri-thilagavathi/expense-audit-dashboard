import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Audit Dashboard", layout="wide")
st.title("💼 Automated Expense Audit Dashboard")

# Upload the Excel file
uploaded_file = st.file_uploader("📤 Upload Expense Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Read Excel file
    df = pd.read_excel(uploaded_file)

    # Clean column names (optional)
    df.columns = df.columns.str.strip().str.title()

    # Show raw data
    st.subheader("📋 Uploaded Expense Data")
    st.dataframe(df, use_container_width=True)

    # Show basic summary
    total_amount = df["Amount"].sum()
    total_entries = df.shape[0]

    col1, col2 = st.columns(2)
    col1.metric("💰 Total Expenses", f"₹{total_amount:,.2f}")
    col2.metric("🧾 Number of Entries", total_entries)
else:
    st.info("Please upload an Excel file to begin.")
# Load known vendor list
vendor_df = pd.read_csv("vendor_master_list.csv")
known_vendors = vendor_df["Vendor"].str.lower().str.strip().tolist()

# Convert date to datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Weekday"] = df["Date"].dt.day_name()

# Rule 1: High value > ₹1,00,000
df["High Amount"] = df["Amount"] > 100000

# Rule 2: Unknown vendor
df["Vendor Clean"] = df["Vendor"].str.lower().str.strip()
df["Unknown Vendor"] = ~df["Vendor Clean"].isin(known_vendors)

# Rule 3: Weekend expenses
df["Weekend"] = df["Weekday"].isin(["Saturday", "Sunday"])

# Combine all flags
df["Flagged"] = df[["High Amount", "Unknown Vendor", "Weekend"]].any(axis=1)

# Show flagged data
st.subheader("🚩 Flagged Suspicious Entries")
flagged = df[df["Flagged"]]
st.dataframe(flagged.drop(columns=["Vendor Clean"]), use_container_width=True)

# Optional: Save flagged results
flagged.to_csv("flagged_output.csv", index=False)
st.subheader("🎛️ Filter Options")

# Unique values for dropdowns
vendors = df["Vendor"].sort_values().unique().tolist()
categories = df["Category"].sort_values().unique().tolist()

# Filter widgets
col1, col2, col3 = st.columns(3)
selected_vendor = col1.selectbox("Filter by Vendor", options=["All"] + vendors)
selected_category = col2.selectbox("Filter by Category", options=["All"] + categories)
selected_flag = col3.selectbox("Show Only", options=["All", "Flagged Only", "Not Flagged"])

# Apply filters
filtered_df = df.copy()

if selected_vendor != "All":
    filtered_df = filtered_df[filtered_df["Vendor"] == selected_vendor]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_flag == "Flagged Only":
    filtered_df = filtered_df[filtered_df["Flagged"] == True]
elif selected_flag == "Not Flagged":
    filtered_df = filtered_df[filtered_df["Flagged"] == False]

# Show filtered data
st.subheader("📌 Filtered Expense Data")
st.dataframe(filtered_df.drop(columns=["Vendor Clean"]), use_container_width=True)
# Download flagged entries
st.subheader("⬇️ Download Flagged Results")
csv = flagged.drop(columns=["Vendor Clean"]).to_csv(index=False).encode("utf-8")
st.download_button("Download Flagged CSV", data=csv, file_name="flagged_entries.csv", mime="text/csv")
import plotly.express as px

st.subheader("📊 Expense Distribution by Category")

category_summary = df.groupby("Category")["Amount"].sum().reset_index()
fig = px.pie(category_summary, values="Amount", names="Category", title="Expense by Category", hole=0.3)
st.plotly_chart(fig, use_container_width=True)
st.subheader("🏆 Top 5 Vendors by Expense Amount")

vendor_summary = df.groupby("Vendor")["Amount"].sum().sort_values(ascending=False).head(5).reset_index()
fig2 = px.bar(vendor_summary, x="Vendor", y="Amount", title="Top 5 Vendors", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)
# Rule 4: GST mismatch based on category
GST_rules = {
    "Office": "18%",
    "Food": "5%",
    "Professional": "18%",
    # Add more as needed
}

