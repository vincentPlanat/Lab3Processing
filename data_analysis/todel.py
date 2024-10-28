import streamlit as st
import pandas as pd
import numpy as np

# Sample data for statistics
data = {
    'Category': ['Sales', 'Sales', 'Sales', 'Profit', 'Profit', 'Profit'],
    'Year': [2020, 2021, 2022, 2020, 2021, 2022],
    'Value': [100, 120, 150, 50, 60, 70]
}
df = pd.DataFrame(data)

# Function to display statistics
def display_statistics(category):
    stats_df = df[df['Category'] == category]
    st.write(f"### {category} Statistics")
    st.write(stats_df)

# Main application
st.title("Statistics Dashboard")

# Select box for category selection
categories = df['Category'].unique()
category = st.selectbox("Select Category", categories)

# Display statistics based on category
display_statistics(category)

# Text input for custom query
custom_query = st.text_input("Enter a custom query (e.g., 'Sales 2021')")

# Display custom query results if input is not empty
if custom_query:
    query_parts = custom_query.split()
    if len(query_parts) == 2 and query_parts[0] in categories and query_parts[1] in df['Year'].astype(str).tolist():
        custom_df = df[(df['Category'] == query_parts[0]) & (df['Year'] == int(query_parts[1]))]
        st.write(f"### Custom Query Results for {custom_query}")
        st.write(custom_df)
    else:
        st.error("Invalid custom query. Please enter in the format 'Category Year'.")

# Multiple options on the left to display different statistics
col1, col2 = st.columns(2)

with col1:
    st.header("Quick Stats")
    if st.button("Display Sales 2022"):
        sales_2022 = df[(df['Category'] == 'Sales') & (df['Year'] == 2022)]
        st.write("### Sales 2022")
        st.write(sales_2022)
    if st.button("Display Profit 2021"):
        profit_2021 = df[(df['Category'] == 'Profit') & (df['Year'] == 2021)]
        st.write("### Profit 2021")
        st.write(profit_2021)

with col2:
    st.header("Additional Stats")
    if st.button("Display Total Sales"):
        total_sales = df[df['Category'] == 'Sales']['Value'].sum()
        st.write(f"### Total Sales: {total_sales}")
    if st.button("Display Total Profit"):
        total_profit = df[df['Category'] == 'Profit']['Value'].sum()
        st.write(f"### Total Profit: {total_profit}")