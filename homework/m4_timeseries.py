"""
M4 時間序列與 EDA — 課後作業
===============d===============
情境：用合併好的訂單資料做時間維度分析，
產出月報級別的商業洞察。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import pandas as pd


def _load_data():
    """輔助函式：讀取並解析日期"""
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                     parse_dates=["order_date"])
    return df


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_avg_by_month():
    """
    計算每個月份 (1~12) 的平均訂單金額
    回傳 Series（index=月份 1~12, values=平均金額）
    提示：df['order_date'].dt.month
    """
    # TODO: 你的程式碼
    df = _load_data
    df['order_date'] = pd.to_datetime(df['order_date'])
    mon = df.groupby(df['order_date'].dt.month)['amount'].mean()
    return mon


def green_top3_dates():
    """
    找出訂單數最多的前 3 個日期
    回傳 Series（index=日期, values=訂單數, 由多到少排序）
    提示：value_counts().head(3)
    """
    # TODO: 你的程式碼
    df = _load_data
    df['order_date'] = pd.to_datetime(df['order_date'])
    # 可能會把不同時間當成不同日期，所以要把時拿掉留下日就好
    df['order_date'] = pd.to_datetime(df['order_date']).dt.date
    top3 = df['order_date'].value_counts().head(3)
    return top3


def green_date_range():
    """
    回傳資料的日期範圍 tuple: (最早日期, 最晚日期)
    格式為 pandas Timestamp
    """
    # TODO: 你的程式碼
    # 這樣就是timestamp型態
    #  dt.date會是 datetime.date的型態
    df = _load_data()
    dates  = pd.to_datetime(df['order_date'])
    return (dates.min(), dates.max())


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_monthly_revenue():
    """
    計算每月總營收
    回傳 Series（index=月底日期 period, values=總營收）
    提示：set_index('order_date').resample('ME')['amount'].sum()
    """
    # TODO: 你的程式碼
    df = _load_data()
    # 確保是datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    #set_index 是把時間變成index 時間序列分系必備
    # resample是時間版的groupby
    rev = df.set_index('order_date').resample('ME')['amount'].sum()
    return rev


def yellow_rolling_avg(monthly_revenue):
    """
    計算 3 個月移動平均
    接收 yellow_monthly_revenue() 的結果作為輸入
    回傳 Series（同樣 index，values=移動平均，前 2 筆可為 NaN）
    提示：.rolling(window=3).mean()
    """
    # TODO: 你的程式碼
    return monthly_revenue.rolling(window = 3).mean()


def yellow_category_median(df):
    """
    計算每個商品類別 (category) 的訂單金額中位數，由高到低排序
    回傳 Series（index=category, values=中位數）
    提示：groupby + median + sort_values
    """
    # TODO: 你的程式碼
    val = df.groupby('category')['amount'].median()
    #val 是一個series，沒有欄位名稱 ，所以要不指定欄位排序
    val = val.sort_values(ascending = False)
    return val


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_monthly_report():
    df = _load_data()

    # datetime
    df['order_date'] = pd.to_datetime(df['order_date'])

    # 設 index
    df = df.set_index('order_date')

    # 每月聚合
    monthly = df.resample('ME').agg({
        'order_id': 'count',
        'amount': 'sum',
        'customer_id': 'nunique'
    })

    # 改欄位名稱
    monthly.columns = [
        'order_count',
        'revenue',
        'active_customers'
    ]

    # 客單價
    monthly['avg_order_value'] = (
        monthly['revenue'] / monthly['order_count']
    )

    # 6成長率
    monthly['revenue_growth'] = (
        monthly['revenue'].pct_change()
    )

    # 7️轉 period
    monthly.index = monthly.index.to_period('M')

    return monthly