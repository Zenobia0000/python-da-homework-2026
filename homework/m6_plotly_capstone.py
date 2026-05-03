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
    df = pd.read_csv(
    '../datasets/ecommerce/orders_enriched.csv',
    parse_dates=['order_date'],)
    region_rev = df.groupby('category', as_index=False)['amount'].sum().sort_values('amount', ascending=False)
    fig = px.bar(region_rev, x='category', y='amount', text='amount',
             color='category', title='Revenue by Category')
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(height=400, showlegend=False)
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    df = pd.read_csv(
    '../datasets/ecommerce/orders_enriched.csv',
    parse_dates=['order_date'],)
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    monthly = df.groupby('month', as_index=False)['amount'].sum()

    fig = px.line(monthly, x='month', y='amount', markers=True,
              title='Monthly Revenue Trend')
    fig.update_layout(height=400)
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
    df = pd.read_csv(
    '../datasets/ecommerce/orders_enriched.csv',
    parse_dates=['order_date'],)
    vip_rev = df.groupby('vip_level', as_index=False)['amount'].sum()
    fig = px.pie(vip_rev, names='vip_level', values='amount',
             title='VIP Level Share', hole=0.4)
    fig.update_layout(height=400)
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
    df = pd.read_csv(
    raw_path,
    parse_dates=['order_date'],)
    df.columns = df.columns.str.strip().str.lower()
    df['amount'] = (
        df['amount'].astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(float)
    )
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    df['qty'] = df['qty'].fillna(df['qty'].median())
    df = df.drop_duplicates()
    customers = pd.read_csv(customers_path)
    products  = pd.read_csv(products_path)

    enriched = (
    df
    .merge(customers, on='customer_id', how='left')
    .merge(products,  on='product_id',  how='left')
)
    return enriched


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
    df = pd.read_csv('../datasets/ecommerce/orders_raw.csv',
    parse_dates=['order_date'],)
    customers = pd.read_csv('../datasets/ecommerce/customers.csv')
    products  = pd.read_csv('../datasets/ecommerce/products.csv')
    df.columns = df.columns.str.strip().str.lower()
    df['amount'] = (
        df['amount'].astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(float)
    )
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    df['qty'] = df['qty'].fillna(df['qty'].median())
    df = df.drop_duplicates()
    
    enriched = (
    df
    .merge(customers, on='customer_id', how='left')
    .merge(products,  on='product_id',  how='left')
    )
    kpis = {
    '總營收':     enriched['amount'].sum(),
    '總訂單數':   len(enriched),
    '活躍顧客數': enriched['customer_id'].nunique(),
    '客單價':     enriched['amount'].sum() / len(enriched),
    }

    return kpis


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
        title='Unit Price vs. Amount by Category'
    )
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
    df = pd.read_csv('../datasets/ecommerce/orders_raw.csv',
    parse_dates=['order_date'],)
    customers = pd.read_csv('../datasets/ecommerce/customers.csv')
    products  = pd.read_csv('../datasets/ecommerce/products.csv')
    df.columns = df.columns.str.strip().str.lower()
    df['amount'] = (
        df['amount'].astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(float)
    )
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    df['qty'] = df['qty'].fillna(df['qty'].median())
    df = df.drop_duplicates()
    
    enriched = (
    df
    .merge(customers, on='customer_id', how='left')
    .merge(products,  on='product_id',  how='left')
    )
    monthly     = enriched.groupby('month', as_index=False)['amount'].sum()
    top_prod    = (enriched.groupby('product_name', as_index=False)['amount']
               .sum().sort_values('amount', ascending=False).head(10))
    region_rev  = enriched.groupby('region', as_index=False)['amount'].sum()
    cat_rev     = enriched.groupby('category', as_index=False)['amount'].sum()
    fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Monthly Revenue Trend',
                    'Top 10 Products',
                    'Revenue by Region',
                    'Category Share'),
    specs=[[{'type': 'xy'},     {'type': 'xy'}],
           [{'type': 'xy'},     {'type': 'domain'}]],
    )

    fig.add_trace(go.Scatter(x=monthly['month'], y=monthly['amount'],
                         mode='lines+markers', name='Monthly'), row=1, col=1)
    fig.add_trace(go.Bar(x=top_prod['product_name'], y=top_prod['amount'],
                     name='Top Products'), row=1, col=2)
    fig.add_trace(go.Bar(x=region_rev['region'], y=region_rev['amount'],
                     name='Region'), row=2, col=1)
    fig.add_trace(go.Pie(labels=cat_rev['category'], values=cat_rev['amount'],
                     name='Category', hole=0.4), row=2, col=2)

    fig.update_layout(
    title_text='<b>E-Commerce Sales Dashboard — 2025【解答版】</b>',
    height=750, showlegend=False,
    )
    fig.update_xaxes(tickangle=45, row=1, col=2)
    return fig
