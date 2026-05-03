"""
M3 Pandas 進階：merge / groupby / RFM — 課後作業
=================================================
情境：你已經有清理好的訂單資料，現在要合併客戶和商品表，
做出有商業價值的分析。

資料路徑：
  - datasets/ecommerce/orders_clean.csv
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd

# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_load_and_merge():
    """
    讀取三張表，合併成一張完整的 DataFrame 並回傳
    """
    df_orders = pd.read_csv('datasets/ecommerce/orders_clean.csv')
    df_customers = pd.read_csv('datasets/ecommerce/customers.csv')
    df_products = pd.read_csv('datasets/ecommerce/products.csv')
    
    # 執行連續合併
    df = pd.merge(df_orders, df_customers, on='customer_id', how='left')
    df = pd.merge(df, df_products, on='product_id', how='left')
    return df


def green_row_count(df):
    """回傳 DataFrame 的列數 (int)"""
    return len(df)


def green_column_list(df):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    return df.columns.tolist()


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_top_category(df):
    """
    哪個商品類別 (category) 的總營收最高？
    """
    # 根據 category 分組，加總 amount 後取最大值的索引
    return df.groupby('category')['amount'].sum().idxmax()


def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    """
    gold_df = df[df['vip_level'] == 'Gold']
    order_count = len(gold_df)
    total_amount = gold_df['amount'].sum()
    return (int(order_count), float(total_amount))


def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    """
    return df.groupby('region')['amount'].mean()


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_rfm_top5(df):
    """
    RFM 分析：找出最有價值的前 5 位客戶
    """
    # 確保日期格式正確，才能計算最近下單日期
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    rfm = df.groupby(['customer_id', 'customer_name']).agg({
        'order_date': 'max',   # Recency: 最近一次日期
        'order_id': 'count',   # Frequency: 訂單總數
        'amount': 'sum'        # Monetary: 消費總額
    }).reset_index()

    # 重命名欄位
    rfm.columns = ['customer_id', 'customer_name', 'R', 'F', 'M']
    
    # 按 M 排序並取前 5
    return rfm.sort_values(by='M', ascending=False).head(5)
