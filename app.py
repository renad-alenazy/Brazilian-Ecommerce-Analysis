import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="تحليل التجارة الإلكترونية", layout="wide")
st.title("📊 تحليل بيانات التجارة الإلكترونية البرازيلية")

# قراءة البيانات من ملفات CSV
@st.cache_data
def load_data():
    orders = pd.read_csv('olist_orders_dataset.csv')
    order_items = pd.read_csv('olist_order_items_dataset.csv')
    products = pd.read_csv('olist_products_dataset.csv')
    customers = pd.read_csv('olist_customers_dataset.csv')
    return orders, order_items, products, customers

orders, order_items, products, customers = load_data()

# Sidebar للتفاعلية
st.sidebar.header("🔍 الفلاتر")
selected_year = st.sidebar.selectbox("اختاري السنة", ["الكل"] + sorted(orders['order_purchase_timestamp'].str[:4].unique()))

# التحليل 1: المبيعات الشهرية مع رسم بياني
st.header("📈 المبيعات الشهرية")

# دمج الجداول
orders_items = orders.merge(order_items, on='order_id')
delivered = orders_items[orders_items['order_status'] == 'delivered']

# تحويل التاريخ
delivered['order_purchase_timestamp'] = pd.to_datetime(delivered['order_purchase_timestamp'])
delivered['month'] = delivered['order_purchase_timestamp'].dt.to_period('M').astype(str)

# حساب الإحصائيات الشهرية
df_monthly = delivered.groupby('month').agg({
    'order_id': 'count',
    'price': 'sum'
}).reset_index()
df_monthly.columns = ['month', 'total_orders', 'total_revenue']
df_monthly['total_revenue'] = df_monthly['total_revenue'].round(2)

col1, col2 = st.columns(2)
with col1:
    st.metric("إجمالي الطلبات", f"{df_monthly['total_orders'].sum():,}")
with col2:
    st.metric("إجمالي الإيرادات", f"${df_monthly['total_revenue'].sum():,.2f}")

fig_revenue = px.line(df_monthly, x='month', y='total_revenue', title='الإيرادات الشهرية', markers=True)
fig_revenue.update_layout(xaxis_title='الشهر', yaxis_title='الإيرادات ($)')st.plotly_chart(fig_revenue, use_container_width=True)

# التحليل 2: أفضل الفئات
st.header("🏆 أفضل فئات المنتجات")

# دمع مع المنتجات
orders_items_products = orders_items.merge(products, on='product_id')
delivered_products = orders_items_products[orders_items_products['order_status'] == 'delivered']

df_categories = delivered_products.groupby('product_category_name').agg({
    'order_id': 'count',
    'price': 'sum'
}).reset_index()
df_categories.columns = ['product_category_name', 'total_sales', 'total_revenue']
df_categories['total_revenue'] = df_categories['total_revenue'].round(2)
df_categories = df_categories.sort_values('total_revenue', ascending=False).head(10)

fig_pie = px.pie(df_categories, values='total_revenue', names='product_category_name', 
                 title='توزيع الإيرادات حسب الفئة', hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# التحليل 3: المدن
st.header("🌍 توزيع العملاء حسب المدينة")

df_cities = customers.groupby('customer_city').size().reset_index(name='customer_count')
df_cities = df_cities.sort_values('customer_count', ascending=False).head(10)

fig_bar = px.bar(df_cities, x='customer_city', y='customer_count', 
                 title='أفضل 10 مدن من حيث عدد العملاء',
                 labels={'customer_city': 'المدينة', 'customer_count': 'عدد العملاء'})
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)

# أسئلة تفاعلية
st.header("❓ اسألي البيانات")
question = st.selectbox("اختاري سؤال:", [
    "ما هو أفضل شهر من حيث المبيعات؟",
    "ما هي الفئة الأكثر مبيعاً؟",
    "ما هي المدينة الأكثر طلباً؟"
])

if question == "ما هو أفضل شهر من حيث المبيعات؟":
    best_month = df_monthly.loc[df_monthly['total_revenue'].idxmax()]
    st.success(f"أفضل شهر: {best_month['month']} بإيرادات ${best_month['total_revenue']:,.2f}")
elif question == "ما هي الفئة الأكثر مبيعاً؟":
    st.success(f"الأفضل: {df_categories.iloc[0]['product_category_name']}")
elif question == "ما هي المدينة الأكثر طلباً؟":
    st.success(f"الأفضل: {df_cities.iloc[0]['customer_city']}")

# عرض البيانات الخامst.header("📋 عرض البيانات")
if st.checkbox("إظهار البيانات الخام"):
    st.dataframe(delivered.head(100))
    st.markdown("---")
st.markdown("تم التطوير بواسطة: رناد العنزي")