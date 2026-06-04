import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="تحليل التجارة الإلكترونية", layout="wide")
st.title("📊 تحليل بيانات التجارة الإلكترونية البرازيلية")

@st.cache_data
def load_data():
    orders = pd.read_csv('olist_orders_dataset.csv')
    order_items = pd.read_csv('olist_order_items_dataset.csv')
    products = pd.read_csv('olist_products_dataset.csv')
    customers = pd.read_csv('olist_customers_dataset.csv')
    return orders, order_items, products, customers

orders, order_items, products, customers = load_data()

st.sidebar.header("🔍 الفلاتر")

st.header("📈 المبيعات الشهرية")
orders_items = orders.merge(order_items, on='order_id')
delivered = orders_items[orders_items['order_status'] == 'delivered'].copy()
delivered['order_purchase_timestamp'] = pd.to_datetime(delivered['order_purchase_timestamp'])
delivered['month'] = delivered['order_purchase_timestamp'].dt.to_period('M').astype(str)

df_monthly = delivered.groupby('month').agg({'order_id': 'count', 'price': 'sum'}).reset_index()
df_monthly.columns = ['month', 'total_orders', 'total_revenue']

col1, col2 = st.columns(2)
with col1:
    st.metric("إجمالي الطلبات", f"{df_monthly['total_orders'].sum():,}")
with col2:
    st.metric("إجمالي الإيرادات", f"${df_monthly['total_revenue'].sum():,.2f}")

# رسم الإيرادات الشهرية - مع تحسينات
fig_revenue = px.line(df_monthly, x='month', y='total_revenue', title='الإيرادات الشهرية', markers=True)
fig_revenue.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20), hovermode='x unified')
st.plotly_chart(fig_revenue, use_container_width=True, key='chart1')

st.header("🏆 أفضل فئات المنتجات")
orders_items_products = orders_items.merge(products, on='product_id')
delivered_products = orders_items_products[orders_items_products['order_status'] == 'delivered']

df_categories = delivered_products.groupby('product_category_name').agg({'order_id': 'count', 'price': 'sum'}).reset_index()
df_categories.columns = ['product_category_name', 'total_sales', 'total_revenue']
df_categories = df_categories.sort_values('total_revenue', ascending=False).head(10)

# رسم الفئات - مع تحسينات
fig_pie = px.pie(df_categories, values='total_revenue', names='product_category_name', title='توزيع الإيرادات حسب الفئة', hole=0.4)
fig_pie.update_layout(height=500, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_pie, use_container_width=True, key='chart2')

st.header("🌍 توزيع العملاء حسب المدينة")
df_cities = customers.groupby('customer_city').size().reset_index(name='customer_count')
df_cities = df_cities.sort_values('customer_count', ascending=False).head(10)

# رسم المدن - مع تحسينات
fig_bar = px.bar(df_cities, x='customer_city', y='customer_count', title='أفضل 10 مدن', labels={'customer_city': 'المدينة', 'customer_count': 'عدد العملاء'})
fig_bar.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20), xaxis_tickangle=-45, hovermode='x unified')
st.plotly_chart(fig_bar, use_container_width=True, key='chart3')

st.markdown("---")
st.markdown("تم التطوير بواسطة: Renad Alenazy")
