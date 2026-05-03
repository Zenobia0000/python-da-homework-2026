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
    - orders_clean.csv LEFT JOIN customers.csv ON customer_id
    - 再 LEFT JOIN products.csv ON product_id
    提示：pd.merge(how='left')
    """
    # TODO: 你的程式碼
    #pass
    order = pd.read_csv("datasets/ecommerce/orders_clean.csv")
    customer = pd.read_csv("datasets/ecommerce/customers.csv")
    prod = pd.read_csv("datasets/ecommerce/products.csv")
    df = ( 
        order.merge(customer, how='left', on='customer_id')
        .merge(prod, how='left', on='product_id')
    )
    return df
    


def green_row_count(df:pd.DataFrame):
    """回傳 DataFrame 的列數 (int)"""
    # TODO: 你的程式碼
    #pass
    return df.shape[0]


def green_column_list(df:pd.DataFrame):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    # TODO: 你的程式碼
    #pass
    return df.columns.tolist()


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_top_category(df:pd.DataFrame):
    """
    哪個商品類別 (category) 的總營收最高？
    回傳該類別名稱 (str)
    提示：groupby('category')['amount'].sum()
    """
    # TODO: 你的程式碼
    #pass
    return df.groupby('category')['amount'].sum().idxmax()


def yellow_gold_vip_stats(df:pd.DataFrame):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    提示：df[df['vip_level'] == 'Gold']
    """
    # TODO: 你的程式碼
    #pass
    mask = (df['vip_level'] == 'Gold')
    return (mask.sum(), df[mask]['amount'].sum())



def yellow_region_avg_amount(df:pd.DataFrame):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
    提示：groupby('region')['amount'].mean()
    """
    # TODO: 你的程式碼
    #pass
    region = df.groupby('region')['amount'].mean()
    region.name = '平均金額'
    return region


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_rfm_top5(df:pd.DataFrame):
    """
    RFM 分析：找出最有價值的前 5 位客戶

    計算每位客戶的：
    - R (Recency)：最近一次下單日期
    - F (Frequency)：訂單總數
    - M (Monetary)：消費總金額

    回傳 DataFrame：
    - 欄位：customer_id, customer_name, R, F, M
    - 按 M 由大到小排序
    - 只取前 5 筆

    提示：groupby('customer_id').agg(...)
    """
    # TODO: 你的程式碼
    #pass
    rfm_h5 = df.groupby('customer_id').agg(R=('order_date','max'),
                              F=('order_id','count'),
                              M=('amount','sum')).reset_index().sort_values('M', ascending=False).head(5)
    rfm_ans = rfm_h5.merge(df[['customer_name','customer_id']], how='left', on='customer_id').drop_duplicates()
    return rfm_ans
