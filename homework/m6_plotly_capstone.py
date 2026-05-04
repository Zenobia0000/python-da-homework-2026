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

    category_revenue = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        category_revenue,
        x="category",
        y="amount",
        title="Total Revenue by Category",
        labels={
            "category": "Category",
            "amount": "Revenue"
        }
    )

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
        "datasets/ecommerce/orders_enriched.csv",
        parse_dates=["order_date"]
    )

    monthly_revenue = (
        df.set_index("order_date")
        .resample("ME")["amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_revenue,
        x="order_date",
        y="amount",
        title="Monthly Revenue Trend",
        labels={
            "order_date": "Month",
            "amount": "Revenue"
        }
    )

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

    vip_counts = (
        df["vip_level"]
        .value_counts()
        .reset_index()
    )

    vip_counts.columns = ["vip_level", "order_count"]

    fig = px.pie(
        vip_counts,
        names="vip_level",
        values="order_count",
        title="Order Share by VIP Level"
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
    # TODO: 你的程式碼
def yellow_clean_and_merge(raw_path, customers_path, products_path):
    # 讀取三份資料
    orders = pd.read_csv(raw_path)
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)

    # 1. 清理欄位名稱：去除前後空白、轉小寫
    orders.columns = orders.columns.str.strip().str.lower()
    customers.columns = customers.columns.str.strip().str.lower()
    products.columns = products.columns.str.strip().str.lower()

    # 2. 清理 amount：去掉 $ 和逗號，再轉成 float
    orders["amount"] = (
        orders["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("", pd.NA)
        .astype(float)
    )

    # 3. 日期轉 datetime，錯誤日期變成 NaT
    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    # 4. 刪除 amount 或 order_date 缺失的資料
    orders = orders.dropna(subset=["amount", "order_date"])

    # 5. 去除重複資料
    orders = orders.drop_duplicates()

    # 6. 合併 customers
    df = pd.merge(
        orders,
        customers,
        on="customer_id",
        how="left"
    )

    # 7. 合併 products
    df = pd.merge(
        df,
        products,
        on="product_id",
        how="left"
    )

    return df


def yellow_kpi_summary(df):
    """
    計算 4 個核心 KPI，回傳 dict
    """
    total_revenue = df["amount"].sum()
    order_count = len(df)
    active_customers = df["customer_id"].nunique()
    avg_order_value = total_revenue / order_count

    return {
        "total_revenue": float(total_revenue),
        "order_count": int(order_count),
        "active_customers": int(active_customers),
        "avg_order_value": float(avg_order_value),
    }


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖
    """
    fig = px.scatter(
        df,
        x="unit_price",
        y="amount",
        color="category",
        hover_data=["product_name"],
        title="Unit Price vs Order Amount",
        labels={
            "unit_price": "Unit Price",
            "amount": "Order Amount",
            "category": "Category",
            "product_name": "Product Name"
        }
    )

    return fig


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
    pass
