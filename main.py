import pandas as pd
import plotly.express as px
import streamlit as st
import random
from config import sample_country, sample_channel, sample_item

# --- config ---
st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide"
                   )

df = pd.read_csv('Sales_Records.csv')
df = df.assign(rating=[random.uniform(1, 10) for i in range(len(df['Country']))])
df.columns = df.columns.str.replace(' ', '_')
df['year'] = pd.DatetimeIndex(df['Order_Date']).year
# --- sidebar ---
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique(),
    default=sample_country
)

sales_channel = st.sidebar.multiselect(
    "Select the Sales Channel:",
    options=df["Sales_Channel"].unique(),
    default=sample_channel
)
item_type = st.sidebar.multiselect(
    "Select the Item Type:",
    options=df["Item_Type"].unique(),
    default=sample_item
)

df_selection = df.query(
    "Country == @country & Item_Type == @item_type & Sales_Channel == @sales_channel "
)

# --- main ---
st.title(":chart_with_upwards_trend: Sales Dashboard")
st.markdown("##")

# TOP KPI'S
total_sales = int(df_selection["Total_Cost"].sum())
average_rating = round(df_selection["rating"].mean(), 1)
star_rating = ":star:"*int(round(average_rating))
average_sale_by_transaction = round(df_selection["Total_Cost"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating}{star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction:,}")

st.markdown("---")

# Sales by item [Bar Chart]
sales_by_item = df_selection.groupby(by=["Item_Type"]).sum()[["Total_Cost"]].sort_values(by="Total_Cost")

fig_product_sales = px.bar(
    sales_by_item,
    x="Total_Cost",
    y=sales_by_item.index,
    orientation="h",
    title="<b>Sales by Product<b>",
    template="plotly_dark",
)
# Sales by year [Bar Chart]
sales_by_year = df_selection.groupby(by=["year"]).sum()[["Total_Cost"]].sort_values(by="Total_Cost")
fig_yearly_sales = px.bar(
    sales_by_year,
    x=sales_by_year.index,
    y="Total_Cost",
    title="<b>Sales by year<b>",
    template="plotly_dark",
)


left_col, right_col = st.columns(2)
with left_col:
    st.plotly_chart(fig_product_sales, use_container_width=True)
with right_col:
    st.plotly_chart(fig_yearly_sales, use_container_width=True)

st.markdown("##")
st.dataframe(df_selection)