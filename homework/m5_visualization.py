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

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=df,
        x="category",
        order=df["category"].value_counts().index,
        ax=ax
    )

    ax.set_title("Order Count by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Order Count")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    df = _load_data()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=df, x="amount", bins=20, ax=ax)

    ax.set_title("Distribution of Order Amount")
    ax.set_xlabel("Amount")
    ax.set_ylabel("Count")

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
    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(["A", "B", "C"], [10, 20, 15])

    ax.set_title("Simple Bar Chart")
    ax.set_xlabel("Group")
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

    df = df[df["region"].isin(["North", "South"])].copy()
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        df.groupby(["month", "region"])["amount"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        data=monthly,
        x="month",
        y="amount",
        hue="region",
        marker="o",
        ax=ax
    )

    ax.set_title("Monthly Revenue Trend: North vs South")
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

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="vip_level", y="amount", ax=ax)

    ax.set_title("Order Amount Distribution by VIP Level")
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

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="unit_price", y="amount", ax=ax)

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

    df_cat = df[df["category"] == category].copy()
    df_cat["month"] = df_cat["order_date"].dt.to_period("M").dt.to_timestamp()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    monthly_revenue = (
        df_cat.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    sns.lineplot(
        data=monthly_revenue,
        x="month",
        y="amount",
        marker="o",
        ax=axes[0, 0]
    )
    axes[0, 0].set_title(f"{category} Monthly Revenue Trend")
    axes[0, 0].set_xlabel("Month")
    axes[0, 0].set_ylabel("Revenue")

    region_revenue = (
        df_cat.groupby("region")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    sns.barplot(
        data=region_revenue,
        x="region",
        y="amount",
        ax=axes[0, 1]
    )
    axes[0, 1].set_title(f"{category} Revenue by Region")
    axes[0, 1].set_xlabel("Region")
    axes[0, 1].set_ylabel("Revenue")

    product_col = "product_name" if "product_name" in df_cat.columns else "product_id"

    top5_products = (
        df_cat.groupby(product_col)["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    sns.barplot(
        data=top5_products,
        x="amount",
        y=product_col,
        ax=axes[1, 0]
    )
    axes[1, 0].set_title(f"{category} Top 5 Products by Revenue")
    axes[1, 0].set_xlabel("Revenue")
    axes[1, 0].set_ylabel("Product")

    sns.histplot(
        data=df_cat,
        x="amount",
        bins=20,
        ax=axes[1, 1]
    )
    axes[1, 1].set_title(f"{category} Order Amount Distribution")
    axes[1, 1].set_xlabel("Amount")
    axes[1, 1].set_ylabel("Count")

    fig.tight_layout()
    return fig