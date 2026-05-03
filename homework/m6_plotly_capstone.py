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
    """
    用 Plotly Express 畫出每個商品類別 (category) 的總營收長條圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.bar()
    """
    # TODO: 你的程式碼
    
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    
    rev_by_cat = df.groupby('category')['amount'].sum().reset_index()
    
    fig = px.bar(rev_by_cat, x='category', y='amount', title="Revenue by Category")
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv", parse_dates=["order_date"])
    
    monthly_rev = df.set_index('order_date').resample('ME')['amount'].sum().reset_index()
    
    fig = px.line(monthly_rev, x='order_date', y='amount', title="Monthly Revenue Trend")
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    
    fig = px.pie(df, names='vip_level', title="VIP Order Distribution")
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：從髒資料到合併完成的 DataFrame
    1. 讀取 orders_raw.csv 並清理（欄位名稱、金額、日期、缺值、去重）
    2. 合併 customers.csv 和 products.csv
    回傳：合併後的 DataFrame
    """
    # TODO: 你的程式碼
    orders = pd.read_csv(raw_path, parse_dates=["order_date"])
    orders = orders.dropna().drop_duplicates() # 去缺值與重複
    
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    
    df = orders.merge(customers, on='customer_id', how='left')
    df = df.merge(products, on='product_id', how='left')
    return df


def yellow_kpi_summary(df):
    """
    計算 4 個核心 KPI，回傳 dict：
    {
        "total_revenue": float,       # 總營收
        "order_count": int,           # 訂單數
        "active_customers": int,      # 不重複客戶數
        "avg_order_value": float,     # 平均客單價
    }
    """
    # TODO: 你的程式碼
    kpi = {
        "total_revenue": float(df['amount'].sum()),
        "order_count": int(df['order_id'].nunique()),
        "active_customers": int(df['customer_id'].nunique()),
        "avg_order_value": float(df['amount'].sum() / df['order_id'].nunique())
    }
    return kpi


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖：
    - X：商品單價 (unit_price)
    - Y：訂單金額 (amount)
    - 顏色：商品類別 (category)
    - hover 顯示：商品名稱 (product_name)
    回傳 plotly Figure 物件
    提示：px.scatter(hover_data=['product_name'])
    """
    # TODO: 你的程式碼
    fig = px.scatter(df, x='unit_price', y='amount', color='category',
                     hover_data=['product_name'], title="Price vs Amount")
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    """
    Capstone：完整的互動式儀表板

    流程：
    1. 清理 orders_raw.csv + 合併三張表
    2. 建立 2×2 subplot dashboard（用 plotly make_subplots）：
       - 左上：月營收趨勢 (line)
       - 右上：Top 10 商品營收 (bar)
       - 左下：各地區營收 (bar)
       - 右下：類別營收佔比 (pie/donut)
    3. 設定整體標題

    回傳 plotly Figure 物件
    提示：from plotly.subplots import make_subplots
    """
    # TODO: 你的程式碼
    df = yellow_clean_and_merge(
        "datasets/ecommerce/orders_raw.csv",
        "datasets/ecommerce/customers.csv",
        "datasets/ecommerce/products.csv"
    )
    
    # 2. 準備 2x2 畫布，並設定子圖類型 (pie 圖需要特別設定 type='domain')
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Monthly Revenue", "Top 10 Products", "Region Revenue", "Category Share"),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "domain"}]]
    )
    
    m_rev = df.set_index('order_date').resample('ME')['amount'].sum().reset_index()
    fig.add_trace(go.Scatter(x=m_rev['order_date'], y=m_rev['amount'], name="Revenue"), row=1, col=1)
    
    top10 = df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(10)
    fig.add_trace(go.Bar(x=top10.index, y=top10.values, name="Top Products"), row=1, col=2)
    
    reg_rev = df.groupby('region')['amount'].sum()
    fig.add_trace(go.Bar(x=reg_rev.index, y=reg_rev.values, name="Region"), row=2, col=1)
    
    cat_rev = df.groupby('category')['amount'].sum()
    fig.add_trace(go.Pie(labels=cat_rev.index, values=cat_rev.values), row=2, col=2)
    
    fig.update_layout(height=800, title_text="E-commerce Executive Dashboard", showlegend=False)
    return fig