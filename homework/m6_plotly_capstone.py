"""
M6 Plotly 互動儀表板 & Capstone — 課後作業
===========================================
情境：從原始資料到互動式儀表板，完成完整的資料分析 pipeline。

資料路徑：
  - datasets/ecommerce/orders_raw.csv（原始髒資料）
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_plotly_bar():
    df = pd.read_csv('orders_enriched.csv')
    # 依照 category 分組計算總營收
    df_cat = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(df_cat, x='category', y='amount', title='每個商品類別的總營收')
    return fig

def green_plotly_line():
    df = pd.read_csv('orders_enriched.csv')
    # 轉換日期並取出月份 (YYYY-MM)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    df_month = df.groupby('month')['amount'].sum().reset_index()
    
    fig = px.line(df_month, x='month', y='amount', title='月營收趨勢圖')
    return fig

def green_plotly_pie():
    df = pd.read_csv('orders_enriched.csv')
    # 計算各 VIP 等級的訂單數量
    fig = px.pie(df, names='vip_level', title='VIP 等級訂單數佔比')
    return fig

# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    # 1. 讀取與清理 orders_raw
    df_orders = pd.read_csv(raw_path)
    df_orders.columns = df_orders.columns.str.strip().str.lower() # 統一欄位名
    df_orders = df_orders.drop_duplicates().dropna() # 去重與去缺值
    
    # 金額與日期轉換
    df_orders['amount'] = pd.to_numeric(df_orders['amount'], errors='coerce')
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce')
    
    # 2. 讀取維度表
    df_customers = pd.read_csv(customers_path)
    df_products = pd.read_csv(products_path)
    
    # 3. 合併 (Merge)
    df_merged = df_orders.merge(df_customers, on='customer_id', how='left')
    df_merged = df_merged.merge(df_products, on='product_id', how='left')
    
    return df_merged

def yellow_kpi_summary(df):
    kpis = {
        "total_revenue": float(df['amount'].sum()),
        "order_count": int(df['order_id'].nunique()),
        "active_customers": int(df['customer_id'].nunique()),
        "avg_order_value": float(df['amount'].mean()),
    }
    return kpis

def yellow_plotly_scatter(df):
    fig = px.scatter(
        df, 
        x='unit_price', 
        y='amount', 
        color='category',
        hover_data=['product_name'],
        title='商品單價 vs 訂單金額散佈圖'
    )
    return fig

# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    # 1. 資料處理
    df = yellow_clean_and_merge(
        'datasets/ecommerce/orders_raw.csv', 
        'datasets/ecommerce/customers.csv', 
        'datasets/ecommerce/products.csv'
    )
    df['month'] = df['order_date'].dt.to_period('M').astype(str)

    # 2. 建立 2x2 Subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('月營收趨勢', 'Top 10 商品營收', '各地區營收', '類別營收佔比'),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "domain"}]] # 右下角是圓餅圖，需設定 domain
    )

    # 左上：月營收趨勢 (Line)
    df_month = df.groupby('month')['amount'].sum().reset_index()
    fig.add_trace(go.Scatter(x=df_month['month'], y=df_month['amount'], name='營收'), row=1, col=1)

    # 右上：Top 10 商品 (Bar)
    df_top10 = df.groupby('product_name')['amount'].sum().nlargest(10).reset_index()
    fig.add_trace(go.Bar(x=df_top10['product_name'], y=df_top10['amount'], name='商品'), row=1, col=2)

    # 左下：地區營收 (Bar)
    df_region = df.groupby('region')['amount'].sum().reset_index()
    fig.add_trace(go.Bar(x=df_region['region'], y=df_region['amount'], name='地區'), row=2, col=1)

    # 右下：類別佔比 (Pie/Donut)
    df_cat = df.groupby('category')['amount'].sum().reset_index()
    fig.add_trace(go.Pie(labels=df_cat['category'], values=df_cat['amount'], hole=.3), row=2, col=2)

    # 3. 整體設定
    fig.update_layout(height=800, title_text="電商營收分析儀表板 (Capstone)", showlegend=False)
    
    return fig
