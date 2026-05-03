"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import matplotlib
matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_bar_category():
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    df = _load_data()
    fig, ax = plt.subplots()
    sns.countplot(x="category", data=df, ax=ax)
    ax.set_title("Order Count by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    df = _load_data()
    fig, ax = plt.subplots()
    sns.histplot(df["amount"], bins=20, ax=ax)
    ax.set_title("Distribution of Order Amount")
    ax.set_xlabel("Amount")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    fig, ax = plt.subplots()
    ax.bar(["A", "B", "C"], [10, 20, 15])
    ax.set_title("Simple Bar Chart")
    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    fig.tight_layout()
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_line_region_trend():
    """
    畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
    - X 軸：月份
    - Y 軸：該月總營收
    - 兩條線，有圖例 (legend)
    回傳 matplotlib Figure 物件
    提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
    """
    df = _load_data()

    sub = df[df["region"].isin(["North", "South"])].copy()
    sub["month"] = sub["order_date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        sub.groupby(["month", "region"])["amount"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots()
    sns.lineplot(data=monthly, x="month", y="amount", hue="region", ax=ax)
    ax.set_title("Monthly Revenue Trend (North vs South)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.legend(title="Region")
    fig.tight_layout()
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    df = _load_data()
    fig, ax = plt.subplots()
    sns.boxplot(x="vip_level", y="amount", data=df, ax=ax)
    ax.set_title("Amount Distribution by VIP Level")
    ax.set_xlabel("VIP Level")
    ax.set_ylabel("Amount")
    fig.tight_layout()
    return fig


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    df = _load_data()
    fig, ax = plt.subplots()
    sns.scatterplot(x="unit_price", y="amount", data=df, ax=ax)
    ax.set_title("Unit Price vs Order Amount")
    ax.set_xlabel("Unit Price")
    ax.set_ylabel("Amount")
    fig.tight_layout()
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_category_dashboard(category="Electronics"):
    """
    針對指定類別，畫 2×2 的 subplot dashboard：
    1. 左上：該類別月營收趨勢 (折線圖)
    2. 右上：該類別各地區營收 (長條圖)
    3. 左下：該類別 Top 5 商品營收 (水平長條圖)
    4. 右下：該類別訂單金額分佈 (直方圖)

    回傳 matplotlib Figure 物件
    提示：fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    """
    df = _load_data()
    sub = df[df["category"] == category].copy()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 月營收趨勢
    sub["month"] = sub["order_date"].dt.to_period("M").dt.to_timestamp()
    monthly = sub.groupby("month")["amount"].sum().reset_index()
    sns.lineplot(data=monthly, x="month", y="amount", ax=axes[0, 0])
    axes[0, 0].set_title(f"{category} Monthly Revenue")

    # 2. 各地區營收
    region_rev = sub.groupby("region")["amount"].sum().reset_index()
    sns.barplot(data=region_rev, x="region", y="amount", ax=axes[0, 1])
    axes[0, 1].set_title(f"{category} Revenue by Region")

    # 3. Top 5 商品
    top_products = (
        sub.groupby("product_name")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    sns.barplot(data=top_products, y="product_name", x="amount", ax=axes[1, 0])
    axes[1, 0].set_title(f"Top 5 Products in {category}")

    # 4. 金額分佈
    sns.histplot(sub["amount"], bins=20, ax=axes[1, 1])
    axes[1, 1].set_title(f"{category} Amount Distribution")

    fig.tight_layout()
    return fig