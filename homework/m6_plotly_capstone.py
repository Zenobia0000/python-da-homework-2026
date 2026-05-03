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
    df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
    category_revenue = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(category_revenue, x='category', y='amount', title='各商品類別總營收')
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    monthly_revenue = df.groupby('month')['amount'].sum().reset_index()
    fig = px.line(monthly_revenue, x='month', y='amount', title='月營收趨勢')
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
    vip_orders = df.groupby('vip_level').size().reset_index(name='count')
    fig = px.pie(vip_orders, values='count', names='vip_level', title='VIP 等級訂單數佔比')
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
    # 讀取資料
    orders = pd.read_csv(raw_path)
    
    # 清理欄位名稱
    orders.columns = orders.columns.str.strip()
    
    # 清理 amount：移除 $ 和 , 轉 float
    orders['amount'] = orders['amount'].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
    
    # 填補 qty 缺值為 1
    orders['qty'] = orders['qty'].fillna(1).astype(int)
    
    # 清理 order_date，drop 空值
    orders = orders.dropna(subset=['order_date'])
    
    # 去重
    orders = orders.drop_duplicates()
    
    # rename 欄位以匹配
    orders = orders.rename(columns={'Order_ID': 'order_id', 'Product_ID': 'product_id'})
    
    # 讀取其他表
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    
    # 合併
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
    total_revenue = df['amount'].sum()
    order_count = df.shape[0]
    active_customers = df['customer_id'].nunique()
    avg_order_value = total_revenue / order_count if order_count > 0 else 0
    
    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "active_customers": active_customers,
        "avg_order_value": avg_order_value,
    }


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
    fig = px.scatter(df, x='unit_price', y='amount', color='category', 
                     hover_data=['product_name'], title='商品單價 vs 訂單金額')
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
    pass