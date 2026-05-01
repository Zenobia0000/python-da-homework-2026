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
    df = pd.read_csv('orders_enriched.csv')
    # 計算每個類別的總營收
    category_revenue = df.groupby('category', as_index=False)['amount'].sum()
    
    fig = px.bar(
        category_revenue, 
        x='category', 
        y='amount', 
        title='各商品類別總營收',
        labels={'category': '商品類別', 'amount': '總營收'}
    )
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    df = pd.read_csv('orders_enriched.csv')
    # 確保日期格式並轉換為「年-月」字串以利分組
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
    
    monthly_revenue = df.groupby('year_month', as_index=False)['amount'].sum()
    
    fig = px.line(
        monthly_revenue, 
        x='year_month', 
        y='amount', 
        markers=True,
        title='月營收趨勢',
        labels={'year_month': '月份', 'amount': '總營收'}
    )
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    df = pd.read_csv('orders_enriched.csv')
    # 計算每個 VIP 等級的訂單數 (算列數或是唯一 order_id)
    vip_counts = df['vip_level'].value_counts().reset_index()
    vip_counts.columns = ['vip_level', 'order_count']
    
    fig = px.pie(
        vip_counts, 
        names='vip_level', 
        values='order_count', 
        title='各 VIP 等級訂單數佔比'
    )
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
    # 1. 讀取原始資料
    orders = pd.read_csv(raw_path)
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    
    # 標準化欄位名稱（轉小寫、去除前後空白）
    orders.columns = orders.columns.str.strip().str.lower()
    
    # 清理金額（移除可能的 $ 或逗號，轉為數值型態）
    if orders['amount'].dtype == 'O':
        orders['amount'] = orders['amount'].str.replace(r'[\$,]', '', regex=True)
    orders['amount'] = pd.to_numeric(orders['amount'], errors='coerce')
    
    # 清理日期（轉換為 datetime，無法轉換的設為 NaT）
    orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
    
    # 處理缺值與去重
    orders = orders.dropna(subset=['order_id', 'amount', 'order_date'])
    orders = orders.drop_duplicates()
    
    # 2. 合併資料
    # 假設 orders 中有 customer_id 和 product_id 可作為 key
    merged_df = orders.merge(customers, on='customer_id', how='left')
    merged_df = merged_df.merge(products, on='product_id', how='left')
    
    return merged_df


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
    total_revenue = float(df['amount'].sum())
    order_count = int(df['order_id'].nunique())
    active_customers = int(df['customer_id'].nunique())
    
    # 避免分母為 0 的錯誤
    avg_order_value = total_revenue / order_count if order_count > 0 else 0.0
    
    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "active_customers": active_customers,
        "avg_order_value": float(avg_order_value)
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
    fig = px.scatter(
        df, 
        x='unit_price', 
        y='amount', 
        color='category', 
        hover_data=['product_name'],
        title='商品單價與訂單金額散佈圖',
        labels={'unit_price': '商品單價', 'amount': '訂單金額', 'category': '商品類別'}
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
    # 1. 取得清理且合併後的資料
    raw_path = "datasets/ecommerce/orders_raw.csv"
    customers_path = "datasets/ecommerce/customers.csv"
    products_path = "datasets/ecommerce/products.csv"
    
    df = yellow_clean_and_merge(raw_path, customers_path, products_path)
    
    # 資料準備
    # 左上：月營收
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
    monthly_rev = df.groupby('year_month')['amount'].sum().reset_index()
    
    # 右上：Top 10 商品營收
    top10_prod = df.groupby('product_name')['amount'].sum().nlargest(10).reset_index()
    
    # 左下：各地區營收
    region_rev = df.groupby('region')['amount'].sum().reset_index()
    
    # 右下：類別營收
    cat_rev = df.groupby('category')['amount'].sum().reset_index()
    
    # 2. 建立 2x2 子圖 (注意右下的圓餅圖需要設定 type 為 'domain')
    fig = make_subplots(
        rows=2, cols=2, 
        subplot_titles=('月營收趨勢', 'Top 10 商品營收', '各地區營收', '類別營收佔比'),
        specs=[[{"type": "xy"}, {"type": "xy"}], 
               [{"type": "xy"}, {"type": "domain"}]]
    )
    
    # 左上：折線圖
    fig.add_trace(
        go.Scatter(x=monthly_rev['year_month'], y=monthly_rev['amount'], mode='lines+markers', name='月營收'),
        row=1, col=1
    )
    
    # 右上：長條圖
    fig.add_trace(
        go.Bar(x=top10_prod['product_name'], y=top10_prod['amount'], name='商品營收'),
        row=1, col=2
    )
    
    # 左下：長條圖
    fig.add_trace(
        go.Bar(x=region_rev['region'], y=region_rev['amount'], name='地區營收'),
        row=2, col=1
    )
    
    # 右下：圓餅圖 / 甜甜圈圖
    fig.add_trace(
        go.Pie(labels=cat_rev['category'], values=cat_rev['amount'], name='類別佔比', hole=0.4),
        row=2, col=2
    )
    
    # 3. 設定整體標題與版面微調
    fig.update_layout(
        title_text="電子商務互動式營運儀表板",
        height=800,
        showlegend=True
    )
    
    return fig
