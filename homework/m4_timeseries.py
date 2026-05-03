"""
M4 時間序列與 EDA — 課後作業
==============================
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
    df = _load_data()
    # 提取月份並計算平均金額
    return df.groupby(df['order_date'].dt.month)['amount'].mean()


def green_top3_dates():
    df = _load_data()
    # 統計日期出現次數並取前三名
    return df['order_date'].value_counts().head(3)


def green_date_range():
    df = _load_data()
    # 取得日期最大與最小值
    return (df['order_date'].min(), df['order_date'].max())


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_monthly_revenue():
    df = _load_data()
    # 以月底為基準重取樣並加總營收
    return df.set_index('order_date')['amount'].resample('ME').sum()


def yellow_rolling_avg(monthly_revenue):
    # 計算 3 個月移動平均
    return monthly_revenue.rolling(window=3).mean()


def yellow_category_median(df):
    # 按類別分組計算中位數並排序
    return df.groupby('category')['amount'].median().sort_values(ascending=False)


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_monthly_report():
    df = _load_data()
    
    # 1. 基礎聚合：訂單數、總營收、不重複客戶數
    report = df.set_index('order_date').resample('ME').agg({
        'order_id': 'count',
        'amount': 'sum',
        'customer_id': 'nunique'
    })
    
    # 2. 重新命名欄位
    report.columns = ['order_count', 'revenue', 'active_customers']
    
    # 3. 計算衍生欄位：客單價與成長率
    report['avg_order_value'] = report['revenue'] / report['order_count']
    report['revenue_growth'] = report['revenue'].pct_change()
    
    return report
