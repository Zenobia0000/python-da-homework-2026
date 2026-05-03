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

gdf:pd.DataFrame
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

def _load_data():
    """輔助函式：讀取資料"""
    global gdf
    gdf = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])
    return gdf 

_load_data()

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
    #pass
    global gdf
    #gdf = _load_data()
    co = gdf['category'].value_counts()
    ax = co.plot(kind='bar',figsize=(10,4),title='Order count in Category',rot=45)
    return plt.gcf()


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    #pass
    global gdf
    fig = plt.figure(figsize=(10,4))
    ax = sns.histplot(gdf['amount'], bins=20, stat='percent', kde=True)
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
    #pass
    global gdf
    reg_order = gdf['region'].value_counts().reset_index()
    fig = plt.figure(figsize=(7,5))
    sns.barplot(data=reg_order, x='region', y='count', palette='viridis', hue='region')
    plt.xlabel('region')
    plt.ylabel('order count')
    plt.title('region vs. order count')
    for r,c in enumerate(reg_order['count']):
        plt.text(r,c, f'{c:,.0f}', ha='center',va='bottom',fontsize=10)
    plt.tight_layout()
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
    #pass
    global gdf
    fig = plt.figure(figsize=(12,4))
    filt = gdf[ gdf['region'].isin(['North','South'])]
    filt['month']= filt['order_date'].dt.to_period('M').astype(str)
    piv = filt.pivot_table(index='region', columns='month', values='amount', aggfunc='sum')
    piv.T
    sns.lineplot(data=piv.T, legend=True, markers='o')
    plt.xticks(rotation=45)
    plt.ylabel('revenue')
    plt.title('North vs. South')
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    #pass
    global gdf
    fig = plt.figure(figsize=(7,4))
    my_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
    sns.boxplot(data=gdf, x='vip_level',y='amount', order=my_order, flierprops={'marker': 'x', 'markeredgecolor': 'red'}) #
    #紅色是離群值
    return fig


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    #pass
    global gdf
    fig = plt.figure(figsize=(7,4))
    sns.scatterplot(data=gdf, x='unit_price', y='amount', hue='region')
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
    #pass
    global gdf
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    category="Electronics"
    filt = gdf[ gdf['category'] == category]
    filt['month'] = filt['order_date'].dt.to_period('M')
    m_a = filt.groupby('month')['amount'].agg('sum').reset_index()
    m_a['month'] = m_a['month'].astype(str)
    sns.lineplot(data=m_a, x='month', y='amount',ax=axes[0,0])
    axes[0,0].tick_params(axis='x', labelrotation=45)
    axes[0,0].legend(
        loc='upper right',       # 放在右上角
        fontsize='small'
    )

    r_a = filt.groupby('region')['amount'].agg('sum').reset_index()
    sns.barplot(data=r_a, x='region', y='amount', ax=axes[0,1])

    p_a = filt.groupby('product_name')['amount'].agg('sum').sort_values(ascending=False).head(5).reset_index()
    # p_a['product_name'] = p_a['product_name'].replace("Data Science Handbook", "Data Science\nHandbook")
    sns.barplot(data=p_a, x='amount', y='product_name', ax=axes[1,0],orient='h')
    axes[1,0].tick_params(axis='x', labelrotation=45)

    filt.head(5)
    sns.histplot(filt['amount'], bins=10, stat='percent',ax=axes[1,1])
    axes[1,1].set_ylabel('Percent(%)')
    return fig