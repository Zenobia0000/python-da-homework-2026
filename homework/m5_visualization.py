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
    barplot = df.groupby("category")["order_id"].count().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 4))
    sns.barplot(data=barplot, x="category", y="order_id")
    plt.title('bar_category', fontweight='bold')
    plt.xlabel('category')
    plt.ylabel('order_count')
    plt.tight_layout()
    fig = plt.gcf()
    return fig
    


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    df = _load_data()
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='amount', bins=20)
    plt.title("Order Amount Distribution")
    plt.tight_layout()
    fig = plt.gcf()
    return fig


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    df = _load_data()
    barplot = df.groupby("region")["order_id"].count().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 4))
    sns.barplot(data=barplot, x="region", y="order_id")
    plt.title("region_order_count", fontweight = "bold", fontsize = 16)
    plt.xlabel("region")
    plt.ylabel("order_count")
    plt.tight_layout()
    fig = plt.gcf()
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
    df['order_date'] = pd.to_datetime(df['order_date'])
    df_filtered = df[df['region'].isin(['North', 'South'])]
    trend_data = df_filtered.groupby(['region', pd.Grouper(key='order_date', freq='ME')])['amount'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=trend_data, x='order_date', y='amount', hue='region', marker='o')
    plt.title('North vs South Monthly Revenue Trend')
    plt.xlabel('Month')
    plt.ylabel('Revenue')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig = plt.gcf()
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    df = _load_data()
    sns.boxplot(x='vip_level', y='amount', data=df, palette='Set3', hue='vip_level', legend=False)
    plt.title('Order Amount Distribution by VIP Level', fontsize=14)
    plt.xlabel('VIP Level', fontsize=12)
    plt.ylabel('Order Amount', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    fig = plt.gcf()
    return fig


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    df = _load_data()
    sns.scatterplot(data=df, x='unit_price', y='amount', alpha=0.5, color='teal')
    plt.title('Relationship between Unit Price and Order Amount', fontsize=14)
    plt.xlabel('Unit Price', fontsize=12)
    plt.ylabel('Order Amount', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    fig = plt.gcf()
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
    # 1. 資料前處理：篩選指定類別並轉換日期
    df['order_date'] = pd.to_datetime(df['order_date'])
    df_cat = df[df['category'] == category].copy()

    # 建立畫布與 2x2 的子圖
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Dashboard: {category} Category Analysis', fontsize=20, fontweight='bold')

    # --- 1. 左上：該類別月營收趨勢 (折線圖) ---
    trend = df_cat.groupby(pd.Grouper(key='order_date', freq='ME'))['amount'].sum().reset_index()
    sns.lineplot(data=trend, x='order_date', y='amount', ax=axes[0, 0], marker='o', color='royalblue')
    axes[0, 0].set_title('Monthly Revenue Trend')
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # --- 2. 右上：該類別各地區營收 (長條圖) ---
    region_rev = df_cat.groupby('region')['amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=region_rev, x='region', y='amount', ax=axes[0, 1], palette='viridis', hue='region', legend=False)
    axes[0, 1].set_title('Revenue by Region')

    # --- 3. 左下：該類別 Top 5 商品營收 (水平長條圖) ---
    top5_prod = df_cat.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(5).reset_index()
    sns.barplot(data=top5_prod, x='amount', y='product_name', ax=axes[1, 0], palette='magma', hue='product_name', legend=False)
    axes[1, 0].set_title('Top 5 Products by Revenue')
    axes[1, 0].set_xlabel('Total Revenue')

    # --- 4. 右下：該類別訂單金額分佈 (直方圖) ---
    sns.histplot(data=df_cat, x='amount', bins=20, ax=axes[1, 1], kde=True, color='seagreen')
    axes[1, 1].set_title('Order Amount Distribution')

    # 優化排版（避免標題與座標軸重疊）
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

    plt.tight_layout()
    fig = plt.gcf()
    return fig