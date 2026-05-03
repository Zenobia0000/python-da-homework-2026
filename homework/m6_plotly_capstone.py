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
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    cat_revenue = df.groupby("category")["amount"].sum().reset_index()
    cat_revenue = cat_revenue.sort_values(by="amount", ascending=False)
    fig = px.bar(
        cat_revenue, 
        x = "category", 
        y = "amount", 
        title = "各類別營收"
        )
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv", parse_dates=["order_date"])
    monthly = df.set_index("order_date").resample("ME")["amount"].sum().reset_index()
    fig = px.line(
        monthly, 
        x = "order_date", 
        y = "amount", 
        title = "月營收趨勢"
        )
    return fig 

def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    vip_counts = df["vip_level"].value_counts().reset_index()
    vip_counts.columns = ["vip_level", "count"]
    fig = px.pie(
        vip_counts, 
        values = "count", 
        names = "vip_level", 
        title = "VIP 等級佔比"
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
    df = pd.read_csv(raw_path)
    df.columns = df.columns.str.strip().str.lower()
    df["amount"] = df["amount"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["amount", "order_date"]).drop_duplicates()

    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    df = df.merge(customers, on="customer_id", how="left")
    df = df.merge(products, on="product_id", how="left")
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
    total_revenue = float(df["amount"].sum())
    order_count = int(len(df))
    active_customers = int(df["customer_id"].nunique())
    avg_order_value = total_revenue / order_count if order_count > 0 else 0.0

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
    fig = px.scatter(
        df, 
        x = "unit_price", 
        y = "amount", 
        color = "category", 
        hover_data = ["product_name"], 
        title = "商品單價 vs 訂單金額"
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
    df = yellow_clean_and_merge(
    "datasets/ecommerce/orders_raw.csv",
    "datasets/ecommerce/customers.csv",
    "datasets/ecommerce/products.csv",
)
    # 左上
    monthly = df.set_index("order_date").resample("ME")["amount"].sum().reset_index()

    # 右上
    top10 = df.groupby("product_name")["amount"].sum().nlargest(10).reset_index()

    # 左下
    by_region = df.groupby("region")["amount"].sum().reset_index()
    # 右下
    by_category = df.groupby("category")["amount"].sum().reset_index()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=["月營收趨勢", "Top10 商品", "各地區營收", "類別佔比"],
        specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "xy"}, {"type": "domain"}]]
    )

    fig.add_trace(go.Scatter(x=monthly["order_date"], y=monthly["amount"], mode="lines"), row=1, col=1)
    fig.add_trace(go.Bar(x=top10["product_name"], y=top10["amount"]), row=1, col=2)
    fig.add_trace(go.Bar(x=by_region["region"], y=by_region["amount"]), row=2, col=1)
    fig.add_trace(go.Pie(labels=by_category["category"], values=by_category["amount"], hole=0.4,), row=2, col=2)

    fig.update_layout(title_text="營運營表板", showlegend=False, height=700)

    return fig