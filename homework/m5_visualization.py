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
    
    return pd.read_csv(
        "datasets/ecommerce/orders_enriched.csv", parse_dates=["order_date"]
    )


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
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["category", "order_count"]

    plt.figure(figsize=(8, 4))
    sns.barplot(
        data=cat_counts,
        x="category",
        y="order_count",
        hue="category",
        palette="viridis",
        legend=False,
    )
    plt.title("Order Count by Category", fontweight="bold")
    plt.xlabel("Category")
    plt.ylabel("Order Count")

    for i, v in enumerate(cat_counts["order_count"]):
        plt.text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    return plt.gcf()


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """

    df = _load_data()
    plt.figure(figsize=(9, 4))
    sns.histplot(data=df, x="amount", bins=30, kde=True, color="steelblue")
    plt.title("Order Amount Distribution", fontweight="bold")
    plt.xlabel("Amount (NT$)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    return plt.gcf()


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    df = _load_data()
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["category", "order_count"]

    plt.figure(figsize=(8, 4))
    sns.barplot(
        data=cat_counts,
        x="category",
        y="order_count",
        hue="category",
        palette="viridis",
        legend=False,
    )
    plt.title("Order Count by Category", fontweight="bold")
    plt.xlabel("Category")
    plt.ylabel("Order Count")
    return plt.gcf()

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
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    ns_df = df[df["region"].isin(["North", "South"])]
    monthly_ns = ns_df.groupby(["month", "region"])["amount"].sum().reset_index()

    plt.figure(figsize=(10, 4))
    sns.lineplot(
        data=monthly_ns,
        x="month",
        y="amount",
        hue="region",
        marker="o",
        linewidth=2,    
    )
    plt.title("Monthly Revenue: North vs South", fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue (NT$)")
    plt.xticks(rotation=45)
    plt.legend(title="Region")
    plt.tight_layout()
    
    return plt.gcf()

def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    df = _load_data()
    plt.figure(figsize=(9, 5))
    sns.boxplot(
        data=df,
        x="vip_level",
        y="amount",
        hue="vip_level",
        palette="Set3",
        legend=False,
    )
    plt.title("Order Amount Distribution by VIP Level", fontweight="bold")
    plt.xlabel("VIP Level")
    plt.ylabel("Amount (NT$)")
    plt.tight_layout()
    return plt.gcf()


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    df = _load_data()

    plt.figure(figsize=(8, 5))

    sns.scatterplot(data=df, x="unit_price", y="amount", alpha=0.5)

    plt.title("Unit Price vs Order Amount")
    plt.xlabel("Unit Price")
    plt.ylabel("Amount")

    plt.tight_layout()
    return plt.gcf()

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
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    elec = df[df["category"] == category].copy()
    # 預先準備四張圖需要的資料
    elec_monthly = elec.groupby("month")["amount"].sum().reset_index()
    elec_region = (
        elec.groupby("region")["amount"].sum().sort_values(ascending=False).reset_index()
    )
    elec_top5 = (
        elec.groupby("product_name")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    # 2x2 儀表板
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Electronics Category Dashboard", fontsize=16, fontweight="bold")

    # (0,0) 月度趨勢
    sns.lineplot(
        data=elec_monthly,
        x="month",
        y="amount",
        marker="o",
        linewidth=2,
        color="#1f77b4",
        ax=axes[0, 0],
    )
    axes[0, 0].set_title("Monthly Revenue Trend")
    axes[0, 0].set_xlabel("Month")
    axes[0, 0].set_ylabel("Revenue (NT$)")
    axes[0, 0].tick_params(axis="x", rotation=45)

    # (0,1) 地區排名
    sns.barplot(
        data=elec_region,
        x="region",
        y="amount",
        hue="region",
        palette="viridis",
        legend=False,
        ax=axes[0, 1],
    )
    axes[0, 1].set_title("Revenue by Region")
    axes[0, 1].set_xlabel("Region")
    axes[0, 1].set_ylabel("Revenue (NT$)")
    for i, v in enumerate(elec_region["amount"]):
        axes[0, 1].text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=9)

    # (1,0) 商品 Top 5
    sns.barplot(
        data=elec_top5,
        y="product_name",
        x="amount",
        hue="product_name",
        palette="magma",
        legend=False,
        ax=axes[1, 0],
    )
    axes[1, 0].set_title("Top 5 Products")
    axes[1, 0].set_xlabel("Revenue (NT$)")
    axes[1, 0].set_ylabel("Product")

    # (1,1) 金額分布
    sns.histplot(
        data=elec,
        x="amount",
        bins=25,
        kde=True,
        color="#d62728",
        ax=axes[1, 1],
    )
    axes[1, 1].set_title("Amount Distribution")
    axes[1, 1].set_xlabel("Amount (NT$)")
    axes[1, 1].set_ylabel("Frequency")

    plt.tight_layout()
    return plt.gcf()
