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
    # TODO: 你的程式碼
    df = _load_data()
    # fig是一張畫布，ax是一張圖
    fig, ax = plt.subplots()
    df['category'].value_counts().plot.bar(ax = ax)
    return fig


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots()
    sns.histplot(df['amount'],bins = 20, ax = ax)
    return fig
    


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots()
    df['category'].value_counts().plot.bar(ax = ax)
    ax.set_xlabel('category') 
    ax.set_ylabel('value')
    ax.set_title('category counts')
    
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
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots()
    df['order_date'] = pd.to_datetime(df['order_date'])
    north = (df[df['region'] == 'North'].set_index('order_date').resample('ME')['amount'].sum())
    south = (df[df['region'] == 'South'].set_index('order_date').resample('ME')['amount'].sum())
    
    ax.plot(north.index, north.values, label='North')
    ax.plot(south.index, south.values, label='South')
    # X,Y軸根標題
    ax.set_xlabel('month')
    ax.set_ylabel('total')
    ax.set_title('Monthly Revenue Trend')
    # 圖例
    ax.legend()
    
    return fig

def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots()
    sns.boxplot(x='vip_level', y='amount', data=df, ax = ax)
    return fig
    
    
    


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots()
    sns.scatterplot(x='unit_price',y='amount',data = df, ax = ax)
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
    # TODO: 你的程式碼
    df = _load_data()
    # 篩選類別
    df = df[df['category'] == category]
    # 篩選時間格式
    df['order_date'] = pd.to_datetime(df['order_date'])
    #建立畫布
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    
    
    # 月營收，左上
    monthly = (df.set_index('order_date').resample('ME')['amount'].sum())
    axes[0, 0].plot(monthly.index,monthly.values)
    axes[0, 0].set_title('monthly revenue')
    
    
    
    # 各地區
    reg_rev = df.groupby('region')['amount'].sum()
    #法一:reg_rev.plot.bar(ax=axes[0, 1]) pandas幫我包好的
    #法二如下:
    axes[0, 1].bar(reg_rev.index, reg_rev.values)
    axes[0, 1].set_title("Revenue by Region")
    
    # 水平長條圖
    top5 = df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(5)
    axes[1, 0].set_title("top5 product revenue")
    # 因為是barh所以(y,x)
    axes[1, 0].barh(top5.values, top5.index)
    
    # 右下
    axes[1, 1].hist(df['amount'], bins=20)
    axes[1, 1].set_title("Amount Distribution")
    axes[1, 1].set_xlabel("Amount")
    axes[1, 1].set_ylabel("Count")

    plt.tight_layout()

    return fig
