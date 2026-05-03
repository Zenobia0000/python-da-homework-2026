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


import numpy as np
DATA = './datasets/ecommerce'
orders = pd.read_csv(f'{DATA}/orders_clean.csv',parse_dates=['order_date'])
customers = pd.read_csv(f'{DATA}/customers.csv')
products = pd.read_csv(f'{DATA}/products.csv')
def green_load_and_merge():
    """
    讀取三張表，合併成一張完整的 DataFrame 並回傳
    - orders_clean.csv LEFT JOIN customers.csv ON customer_id
    - 再 LEFT JOIN products.csv ON product_id
    提示：pd.merge(how='left')
    """
    # TODO: 你的程式碼
    full = (
        orders
        .merge(customers, on='customer_id', how='left')
        .merge(products, on='product_id', how='left')
    )
    print('三表合併後形狀', full.shape)
    print('欄位', list(full.columns))
    return full
df_final = green_load_and_merge()
df_final.head() 

import numpy as np
DATA = './datasets/ecommerce'
orders = pd.read_csv(f'{DATA}/orders_clean.csv',parse_dates=['order_date'])
customers = pd.read_csv(f'{DATA}/customers.csv')
products = pd.read_csv(f'{DATA}/products.csv')
def green_row_count(df):
    """回傳 DataFrame 的列數 (int)"""
    return len(df)
    # TODO: 你的程式碼
print('orders:' , orders.shape)
print('customers:', customers.shape)
print('products:' , products.shape)


import numpy as np
DATA = './datasets/ecommerce'
orders = pd.read_csv(f'{DATA}/orders_clean.csv',parse_dates=['order_date'])
customers = pd.read_csv(f'{DATA}/customers.csv')
products = pd.read_csv(f'{DATA}/products.csv')
def green_columns(df):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    return list(df.columns)
    # TODO: 你的程式碼
print('orders:' , list(orders.columns))
print('customers:', list(customers.columns))
print('products:' , list(products.columns))


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================


def yellow_top_category(df):
    """
    哪個商品類別 (category) 的總營收最高？
    回傳該類別名稱 (str)
    提示：groupby('category')['amount'].sum()
    """
    # TODO: 你的程式碼
    category_summary = (
        df.groupby(['category'])['amount']
        .sum()
        .reset_index()
        .sort_values(['amount'],ascending=[False])
    )
    top_cat = category_summary.iloc[0]['category']
    return top_cat
result = yellow_top_category(df_final)
print(result)


def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    提示：df[df['vip_level'] == 'Gold']
    """
    # TODO: 你的程式碼
    gold =df[df['vip_level'] == 'Gold']
    gold_stat = gold['amount'].agg(['count','sum'])
    order_count = int(gold_stat['count'])
    total_amount = float(gold_stat['sum'])
    print(f"訂單數:{int(gold_stat['count'])}")
    print(f"總金額:{gold_stat['sum']:,.0f}")
    return (order_count, total_amount)
result = yellow_gold_vip_stats(df_final)


def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
    提示：groupby('region')['amount'].mean()
    """
    # TODO: 你的程式碼
    region_mean = (
        df.groupby('region')['amount']
        .mean()
        .round(2)
        .sort_values(ascending=False)
    )
    print(region_mean)
    return region_mean
result_series = yellow_region_avg_amount(df_final)
    


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_rfm_top5(df):
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
    pass
