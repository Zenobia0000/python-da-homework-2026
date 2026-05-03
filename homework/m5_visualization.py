"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
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
    df = _load_data()
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='category', ax=ax)
    return fig

def green_hist_amount():
    df = _load_data()
    fig, ax = plt.subplots()
    sns.histplot(df['amount'], bins=20, ax=ax)
    return fig

def green_set_labels():
    df = _load_data()
    fig, ax = plt.subplots()
    df['category'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title("Order Count by Category")
    ax.set_xlabel("Category Name")
    ax.set_ylabel("Number of Orders")
    return fig

# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_line_region_trend():
    df = _load_data()
    # 建立月份欄位並過濾區域
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    plot_df = df[df['region'].isin(['North', 'South'])]
    
    # 聚合資料
    trend = plot_df.groupby(['month', 'region'])['amount'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=trend, x='month', y='amount', hue='region', marker='o', ax=ax)
    plt.xticks(rotation=45)
    return fig

def yellow_box_vip():
    df = _load_data()
    fig, ax = plt.subplots()
    sns.boxplot(x='vip_level', y='amount', data=df, ax=ax, order=['Bronze', 'Silver', 'Gold', 'Platinum'])
    return fig

def yellow_scatter_price_amount():
    df = _load_data()
    fig, ax = plt.subplots()
    sns.scatterplot(x='unit_price', y='amount', data=df, ax=ax, alpha=0.5)
    return fig

# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_category_dashboard(category="Electronics"):
    df = _load_data()
    sub_df = df[df['category'] == category].copy()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Dashboard: {category}", fontsize=16)

    # 1. 左上：該類別月營收趨勢 (折線圖)
    sub_df['month'] = sub_df['order_date'].dt.to_period('M').astype(str)
    monthly_rev = sub_df.groupby('month')['amount'].sum()
    monthly_rev.plot(kind='line', marker='o', ax=axes[0, 0])
    axes[0, 0].set_title("Monthly Revenue Trend")

    # 2. 右上：該類別各地區營收 (長條圖)
    sns.barplot(x='region', y='amount', data=sub_df, estimator=sum, errorbar=None, ax=axes[0, 1])
    axes[0, 1].set_title("Revenue by Region")

    # 3. 左下：該類別 Top 5 商品營收 (水平長條圖)
    top5 = sub_df.groupby('product_name')['amount'].sum().nlargest(5)
    top5.plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title("Top 5 Products by Revenue")

    # 4. 右下：該類別訂單金額分佈 (直方圖)
    sns.histplot(sub_df['amount'], bins=15, kde=True, ax=axes[1, 1])
    axes[1, 1].set_title("Order Amount Distribution")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig
