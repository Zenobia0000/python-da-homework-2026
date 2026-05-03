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
    orders = pd.read_csv("datasets/ecommerce/orders_clean.csv")
    customers = pd.read_csv("datasets/ecommerce/customers.csv")
    products = pd.read_csv("datasets/ecommerce/products.csv")
    df = (
            orders
            .merge(customers, on = 'customer_id', how='left')
            .merge(products, on = 'product_id', how='left')
    )
    return df

def green_row_count(df):
    """回傳 DataFrame 的列數 (int)"""
    # TODO: 你的程式碼
    orders = pd.read_csv("datasets/ecommerce/orders_clean.csv")
    customers = pd.read_csv("datasets/ecommerce/customers.csv")
    products = pd.read_csv("datasets/ecommerce/products.csv")
    df = (
            orders
            .merge(customers, on = 'customer_id', how='left')
            .merge(products, on = 'product_id', how='left')
    )
    return df.shape[0]


def green_column_list(df):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    # TODO: 你的程式碼
    return df.columns.tolist()


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
    return df.groupby('category')['amount'].sum().idxmax()


def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    提示：df[df['vip_level'] == 'Gold']
    """
    # TODO: 你的程式碼

    vip = df[df['vip_level'] == 'Gold']
    vip_sum = len(vip['order_id'])
    vip_amount = float(vip['amount'].sum())
    Gold_Vip = (vip_sum, vip_amount)
    return Gold_Vip


def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
    提示：groupby('region')['amount'].mean()
    """
    # TODO: 你的程式碼

    Series = df.groupby('region')['amount'].mean()
    return Series


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
    orders = pd.read_csv("datasets/ecommerce/orders_clean.csv")
    customers = pd.read_csv("datasets/ecommerce/customers.csv")
    products = pd.read_csv("datasets/ecommerce/products.csv")
    # R = orders.groupby('customer_id')['order_date'].max()
    # F = orders.groupby('customer_id')['order_id'].count()
    # M = orders.groupby('customer_id')['amount'].sum().sort_values(ascending=False).head()
    # df = (
    #             orders
    #             .merge(customers, on = 'customer_id', how='left')
    #             .merge(products, on = 'product_id', how='left')
    #     )
    RFM = (
        orders.groupby('customer_id')
        .agg(
            R=('order_date', 'max'),
            F=('order_id', 'count'),
            M=('amount', 'sum'),
        )
        .reset_index()
    )
    rfm_named = RFM.merge(
        customers[['customer_id', 'customer_name']],
        on='customer_id',
        how='left',
    )
    final_5 = (
        rfm_named
        .sort_values('M', ascending=False)
        .head(5)
        .reset_index(drop=True)
        [['customer_id', 'customer_name', 'R', 'F', 'M']]
    )
    return final_5