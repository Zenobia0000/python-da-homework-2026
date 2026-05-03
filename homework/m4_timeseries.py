"""
M4 時間序列與 EDA — 課後作業
==============================
情境：用合併好的訂單資料做時間維度分析，
產出月報級別的商業洞察。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import pandas as pd

gdf:pd.DataFrame

def _load_data():
    """輔助函式：讀取並解析日期"""
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                     parse_dates=["order_date"])
    global gdf
    gdf = df
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
    #pass
    global gdf
    gdf['月份'] = gdf['order_date'].dt.month
    month_avg = gdf.groupby('月份')['amount'].mean()
    month_avg.name = '平均金額'
    return month_avg


def green_top3_dates():
    """
    找出訂單數最多的前 3 個日期
    回傳 Series（index=日期, values=訂單數, 由多到少排序）
    提示：value_counts().head(3)
    """
    # TODO: 你的程式碼
    #pass
    global gdf
    date_ord = gdf['order_date'].value_counts()
    date_ord = date_ord.rename_axis('日期')
    date_ord.name='訂單數'
    return date_ord


def green_date_range():
    """
    回傳資料的日期範圍 tuple: (最早日期, 最晚日期)
    格式為 pandas Timestamp
    """
    # TODO: 你的程式碼
    #pass
    global gdf
    dmax = gdf['order_date'].max()
    dmin = gdf['order_date'].min()
    return dmin, dmax


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
    #pass
    global gdf
    ts = gdf.set_index('order_date').sort_index()
    return ts['amount'].resample('ME').sum()


def yellow_rolling_avg(monthly_revenue:pd.Series):
    """
    計算 3 個月移動平均
    接收 yellow_monthly_revenue() 的結果作為輸入
    回傳 Series（同樣 index，values=移動平均，前 2 筆可為 NaN）
    提示：.rolling(window=3).mean()
    """
    # TODO: 你的程式碼
    #pass
    return monthly_revenue.rolling(window=3).mean()


def yellow_category_median(df:pd.DataFrame):
    """
    計算每個商品類別 (category) 的訂單金額中位數，由高到低排序
    回傳 Series（index=category, values=中位數）
    提示：groupby + median + sort_values
    """
    # TODO: 你的程式碼
    #pass
    cat_med = df.groupby('category')['amount'].median().sort_values
    cat_med.name = '中位數'
    return cat_med


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_monthly_report():
    """
    產出月報 DataFrame，每月一列，包含：
    - order_count：當月訂單數
    - revenue：當月總營收
    - active_customers：當月不重複客戶數
    - avg_order_value：客單價（revenue / order_count）
    - revenue_growth：月營收成長率（相對上月的 % 變化）

    index 為月份 (period 或 datetime)
    提示：resample + agg + pct_change
    """
    # TODO: 你的程式碼
    #pass
    global gdf
    ts = gdf.set_index('order_date').sort_index()
    mon_report = ts.resample('ME').agg(
            order_count=('order_id','count'),
            active_customer=('customer_id','nunique'),
            revenue=('amount','sum'),
            avg_order_value=('amount','mean')
        )
    mon_report['revenue_growth'] = mon_report['revenue'].pct_change()
    return mon_report

