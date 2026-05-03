"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import matplotlib
# matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])

# 顯示中文
sns.set_theme(style='whitegrid')
plt.rcParams['font.family'] = 'Microsoft JhengHei'  # Windows 正黑體
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_bar_category():
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    #axes = sns.countplot(x='category', data=df)
    axes = _load_data()['category'].value_counts().plot.bar()
    return axes.figure



def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    axes = sns.histplot(x="amount", data=_load_data(), bins=20)
    return axes.get_figure()



def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    fig = plt.figure(figsize=(8, 4))
    sns.barplot(data=_load_data(), x='vip_level', y='amount', palette='Set2', hue='vip_level')
    plt.title("不同客戶級別消費力", loc="center")
    plt.xlabel("客戶等級")
    plt.ylabel("總金額")
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
    north = df[df['region'] == 'North'].groupby(df['order_date'].dt.month)['amount'].sum()
    south = df[df['region'] == 'South'].groupby(df['order_date'].dt.month)['amount'].sum()

    fig = plt.figure()
    plt.plot(north.index, north.values, label='North')
    plt.plot(south.index, south.values, label='South')
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    fig = plt.figure()
    sns.boxplot(x='vip_level', y='amount', data=_load_data())
    return fig



def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    fig = plt.figure()
    sns.scatterplot(x='unit_price', y='amount', data=_load_data())
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
    df2 = df[df['category'] == category]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    # 左上：該類別月營收趨勢 (折線圖)
    monthly = df2.groupby(df2['order_date'].dt.month)['amount'].sum()
    axes[0, 0].plot(monthly.index, monthly.values)

    # 右上：該類別各地區營收 (長條圖)
    region = df2.groupby('region')['amount'].sum()
    axes[0, 1].bar(region.index, region.values)

    # 左下：該類別 Top 5 商品營收 (水平長條圖)
    top5 = df2.groupby('product_name')['amount'].sum().nlargest(5).sort_values(ascending=True)
    axes[1, 0].barh(top5.index, top5.values)

    # 右下：該類別訂單金額分佈 (直方圖)
    axes[1, 1].hist(df2['amount'])

    return fig

