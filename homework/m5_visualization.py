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

def green_bar_category(df):
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    # TODO: 你的程式碼
    cat_counts = df['category'].value_counts().reset_index()
    cat_counts.columns = ['category','order_count']
    fig = plt.figure(figsize=(8,4))
    sns.barplot(
        data=cat_counts,
        x='category', y='order_count',
        hue='category', palette='viridis', legend=False,
    )
    plt.title('Order Count by Category', fontweight='bold')
    plt.xlabel('Category')
    plt.ylabel('Order Count')

    for i, v in enumerate(cat_counts['order_count']):
        plt.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    return fig
# green_bar_category()


def green_hist_amount(df):
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    fig=plt.figure(figsize=(9,4))
    sns.histplot(data=df, x='amount', bins=30, kde=True, color='steelblue')
    plt.title('Order Amount Distribution', fontweight='bold')
    plt.xlabel('Amount (NT$)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    return fig
# green_hist_amount()

def green_set_labels(df):
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    # TODO: 你的程式碼
    region_rev = df.groupby('region')['amount'].sum().sort_values(ascending=False).reset_index()

    fig = plt.figure(figsize=(8,4))
    sns.barplot(data=region_rev, x='region', y='amount', palette='viridis', hue='region', legend=False)
    plt.title('Revenue by Region', fontweight='bold')
    plt.xlabel('Region')
    plt.ylabel('Revenue (NT$)')

    for i, v in enumerate(region_rev['amount']):
        plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    return fig
# green_set_labels()


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================
def yellow_line_region_trend(df):
    """
    畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
    - X 軸：月份
    - Y 軸：該月總營收
    - 兩條線，有圖例 (legend)
    回傳 matplotlib Figure 物件
    提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
    """
    # TODO: 你的程式碼
    ns_df = df[df['region'].isin(['North', 'South'])]
    monthly_ns = (
        ns_df.groupby(['month', 'region'])['amount']
        .sum()
        .reset_index()
    )
    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(
        data = monthly_ns,
        x='month', y='amount',
        hue='region',
        marker='o',
        linewidth=2,
    )
    plt.title("Monthly Revenue: North vs South", fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Revenue (NT$)')
    plt.xticks(rotation=45)
    plt.legend(title="Region")
    plt.tight_layout()
    return fig
yellow_line_region_trend()


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    fig = plt.figure(figsize=(9, 5))
    sns.boxplot(
        data=df,
        x='vip_level',
        y='amount',
        hue='vip_level',
        palette='Set3',
        legend=False,
    )
    plt.title('Order Amount Distribution by VIP Level', fontweight='bold')
    plt.xlabel('VIP Level')
    plt.ylabel('Amount (NT$)')
    plt.tight_layout()
    return fig
yellow_box_vip()

def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    fig = plt.figure(figsize=(9, 5))
    sns.scatterplot(
        data=df, 
        x='unit_price', 
        y='amount',
        hue='category',
        alpha=0.6, s=60)
    plt.title('Unit Price vs Order Amount (by Category)', fontweight='bold')
    plt.xlabel("Unit Price")
    plt.ylabel("Order Amount")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    return fig
yellow_scatter_price_amount()


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
    pass
