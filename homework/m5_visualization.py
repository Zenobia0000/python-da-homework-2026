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
    return pd.read_csv("../datasets/ecommerce/orders_enriched.csv",
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
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='category', ax=ax)
    ax.set_title("Order Count by Category")
    return fig
    pass


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='amount', bins=20, ax=ax)
    ax.set_title("Distribution of Order Amounts")
    return fig
    pass


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    # TODO: 你的程式碼
    data = {'A': 100, 'B': 200, 'C': 300}
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values())
    ax.set_title("Simple Bar Chart")
    ax.set_xlabel("Category")
    ax.set_ylabel("Values")
    return fig
    pass


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
    # TODO: 你的程式碼
    df = _load_data()
    target_regions = df[df['region'].isin(['North', 'South'])]
    trend_data = target_regions.groupby([target_regions['order_date'].dt.month, 'region'])['amount'].sum().unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=target_regions, x=target_regions['order_date'].dt.month, y='amount', hue='region', estimator='sum', ax=ax)
    ax.set_title("Monthly Revenue Trend: North vs South")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    return fig
    pass


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='vip_level', y='amount', ax=ax)
    ax.set_title("Order Amount Distribution by VIP Level")
    return fig
    pass


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='unit_price', y='amount', ax=ax)
    ax.set_title("Unit Price vs Order Amount")
    return fig
    pass


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
    # TODO: 你的程式碼
    df = _load_data()
    cat_df = df[df['category'] == category].copy()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Dashboard: {category}", fontsize=20)
    monthly_rev = cat_df.set_index('order_date').resample('ME')['amount'].sum()
    axes[0, 0].plot(monthly_rev.index, monthly_rev.values, marker='o', color='b')
    axes[0, 0].set_title("Monthly Revenue Trend")
    axes[0, 0].tick_params(axis='x', rotation=45)

    region_rev = cat_df.groupby('region')['amount'].sum().sort_values(ascending=False)
    sns.barplot(x=region_rev.index, y=region_rev.values, ax=axes[0, 1])
    axes[0, 1].set_title("Revenue by Region")

    top5_prod = cat_df.groupby('product_name')['amount'].sum().nlargest(5)
    sns.barplot(x=top5_prod.values, y=top5_prod.index, ax=axes[1, 0], orient='h')
    axes[1, 0].set_title("Top 5 Products by Revenue")

    sns.histplot(cat_df['amount'], bins=15, kde=True, ax=axes[1, 1])
    axes[1, 1].set_title("Order Amount Distribution")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig
    pass
