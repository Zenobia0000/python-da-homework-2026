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
import plotly.io as pio
from plotly.subplots import make_subplots

pio.templates.default = 'plotly_white'  # 乾淨白底

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
    #pass
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                        parse_dates=["order_date"])
    c_a = df.groupby('category', as_index=False)['amount'].sum()
    fig = px.bar(c_a, x='category',y='amount',text='amount', color='category', title='category vs. amount')
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(height=500, showlegend=False)

    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    #pass
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])
    ts = df.set_index('order_date').sort_index()
    m_a = ts['amount'].resample('ME').sum()
    m_a = m_a.reset_index()
    #m_a
    fig = px.line(m_a, 'order_date', 'amount', markers=True, title='month vs. amount')
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
     #pass
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])
    fig = px.pie(df, 'vip_level')
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
    #pass
    order = pd.read_csv(raw_path)
    customer = pd.read_csv(customers_path)
    product = pd.read_csv(products_path)
    order.columns = order.columns.str.strip().str.lower()
    order['amount'] = order['amount'].str.replace('$','').str.replace(',','').astype(float)
    order['amount'].fillna(order['amount'].median())

    pd.to_datetime(order['order_date'], errors='coerce')

    order = order.dropna(subset=['order_date'])
    order.drop_duplicates()

    df = (
        order
        .merge(customer, how='left', on='customer_id')
        .merge(product, how='left', on='product_id')
    )
    return df


def yellow_kpi_summary(df:pd.DataFrame):
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
    #pass
    t_r = df['amount'].sum()
    o_c = df.shape[0]
    a_c = df['customer_id'].nunique()
    a_o_v = t_r/o_c

    return  {
        "total_revenue": t_r,       # 總營收
        "order_count": o_c,           # 訂單數
        "active_customers": a_c,      # 不重複客戶數
        "avg_order_value": a_o_v,     # 平均客單價
    }


def yellow_plotly_scatter(df:pd.DataFrame):
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
    #pass

    fig = px.scatter(df, 'unit_price', 'amount', hover_data=['product_name'], color='category', title='unit price vs. amount')
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================
from plotly.subplots import make_subplots

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
    #pass
    df = yellow_clean_and_merge('datasets/ecommerce/orders_raw.csv', 
                                'datasets/ecommerce/customers.csv',
                                'datasets/ecommerce/products.csv')
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    m_a = df.groupby('month', as_index=False)['amount'].sum()
    p_a = df.groupby('product_name', as_index=False)['amount'].sum().sort_values('amount',ascending=False).head(10)
    r_a = df.groupby('region', as_index=False)['amount'].sum()
    c_a = df.groupby('category', as_index=False)['amount'].sum()

    fig = make_subplots(2,2, subplot_titles= ('Monthly revenue trend', 'Top 10 Products', 'Revenue by region', 'Category share'), 
                    specs=[ [{'type':'xy'}, {'type':'xy'}], [{'type':'xy'}, {'type':'domain'}] ])
        
    fig.add_trace(go.Scatter(x=m_a['month'], y=m_a['amount'],mode='lines+markers', name='Monthly' ), row=1, col=1)
    fig.add_trace(go.Bar(x=p_a['product_name'], y=p_a['amount']), row=1, col=2)
    fig.add_trace(go.Bar(x=r_a['region'], y=r_a['amount']), row=2, col=1)
    fig.add_trace(go.Pie(labels=c_a['category'], values=c_a['amount'], name='category', hole=0.4), row=2, col=2)

    fig.update_layout(height=800, title_text="Sales Dashboard", showlegend=False)
    # fig.show()
    return fig    

if __name__ == '__main__':
    pass