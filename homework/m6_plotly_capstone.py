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
    df = pd.read_csv("../datasets/ecommerce/orders_enriched.csv")
    cat_revenue = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(
        cat_revenue, 
        x='category', 
        y='amount', 
        title='Total Revenue by Category',
        labels={'amount': 'Total Revenue', 'category': 'Product Category'},
        template='plotly_white')
    return fig
    pass


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("../datasets/ecommerce/orders_enriched.csv")
    monthly_rev = df.set_index('order_date').resample('ME')['amount'].sum().reset_index()
    fig = px.line(
        monthly_rev, 
        x='order_date', 
        y='amount', 
        title='Monthly Revenue Trend',
        labels={'order_date': 'Month', 'amount': 'Monthly Revenue'},
        markers=True)
    return fig
    pass


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("../datasets/ecommerce/orders_enriched.csv")
    fig = px.pie(
        df, 
        names='vip_level', 
        title='Order Distribution by VIP Level',
        hole=0.3)
    return fig
    pass


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：從髒資料到合併完成的 DataFrame
    1. 讀取 orders_raw.csv 並清理（欄位名稱、金額、日期、缺值、去重）
    2. 統一欄位大小寫以解決 Merge 衝突
    3. 合併 customers.csv 和 products.csv
    回傳：合併後的 DataFrame
    """
    # TODO: 你的程式碼
    orders = pd.read_csv(raw_path)
    orders = orders.drop_duplicates()
    orders = orders.dropna(subset=['order_id', 'customer_id'])
    orders.columns = orders.columns.str.lower()
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    if 'amount' in orders.columns:
        orders['amount'] = pd.to_numeric(orders['amount'], errors='coerce').fillna(0)
    customers = pd.read_csv(customers_path)
    customers.columns = customers.columns.str.lower()
    products = pd.read_csv(products_path)
    products.columns = products.columns.str.lower()
    df_merged = orders.merge(customers, on='customer_id', how='left')
    df_merged = df_merged.merge(products, on='product_id', how='left')
    
    return df_merged


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
    total_revenue = float(df['amount'].sum())
    order_count = int(df['order_id'].count())
    active_customers = int(df['customer_id'].nunique())
    avg_order_value = total_revenue / order_count if order_count > 0 else 0.0
    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "active_customers": active_customers,
        "avg_order_value": avg_order_value
    }
    pass


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
    fig = px.scatter(
        df,
        x='unit_price',
        y='amount',
        color='category',
        hover_data=['product_name'],
        title='Product Price vs Order Amount by Category',
        labels={
            'unit_price': 'Unit Price ($)',
            'amount': 'Order Amount ($)',
            'category': 'Product Category'
        },
        template='plotly_white'
    )
    return fig
    pass


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
    orders = pd.read_csv("../datasets/ecommerce/orders_raw.csv").drop_duplicates()
    orders.columns = orders.columns.str.lower()
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    customers = pd.read_csv("../datasets/ecommerce/customers.csv")
    customers.columns = customers.columns.str.lower()
    products = pd.read_csv("../datasets/ecommerce/products.csv")
    products.columns = products.columns.str.lower()
    df = orders.merge(customers, on='customer_id', how='left')
    df = df.merge(products, on='product_id', how='left')

    # 1. 強制將 amount 轉為數字，無法轉換的會變成 NaN
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # 2. 處理可能出現的空值（選用，建議補 0 避免計算錯誤）
    df['amount'] = df['amount'].fillna(0)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Monthly Revenue Trend", 
            "Top 10 Products by Revenue",
            "Revenue by Region", 
            "Revenue Share by Category"
        ),
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "domain"}]]
    )

    monthly_rev = df.set_index('order_date').resample('ME')['amount'].sum().reset_index()
    fig.add_trace(
        go.Scatter(x=monthly_rev['order_date'], y=monthly_rev['amount'], mode='lines+markers', name='Revenue'),
        row=1, col=1
    )

    top10_prod = df.groupby('product_name')['amount'].sum().nlargest(10).reset_index()
    fig.add_trace(
        go.Bar(x=top10_prod['product_name'], y=top10_prod['amount'], name='Product Rev'),
        row=1, col=2
    )

    region_rev = df.groupby('region')['amount'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=region_rev['region'], y=region_rev['amount'], name='Region Rev'),
        row=2, col=1
    )

    cat_rev = df.groupby('category')['amount'].sum().reset_index()
    fig.add_trace(
        go.Pie(labels=cat_rev['category'], values=cat_rev['amount'], hole=0.4, name='Category %'),
        row=2, col=2
    )

    fig.update_layout(
        height=800, 
        width=1000, 
        title_text="E-commerce Business Overview Dashboard",
        showlegend=False,
        template="plotly_white"
    )
    fig.update_xaxes(tickangle=45)
    return fig
    pass
