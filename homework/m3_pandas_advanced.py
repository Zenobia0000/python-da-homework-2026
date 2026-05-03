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

df = (
        pd.read_csv("datasets/ecommerce/orders_clean.csv")
        .merge(pd.read_csv("datasets/ecommerce/customers.csv"), on='customer_id', how='left')
        .merge(pd.read_csv("datasets/ecommerce/products.csv"),  on='product_id',  how='left')
)

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
    df = (
        pd.read_csv("datasets/ecommerce/orders_clean.csv")
        .merge(pd.read_csv("datasets/ecommerce/customers.csv"), on='customer_id', how='left')
        .merge(pd.read_csv("datasets/ecommerce/products.csv"),  on='product_id',  how='left')
    )
    return df

def green_row_count(df):
    """回傳 DataFrame 的列數 (int)"""
    return len(df) # df.shape[0]

def green_column_list(df):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    return df.columns.to_list() # list(df.columns)


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_top_category(df):
    """
    哪個商品類別 (category) 的總營收最高？
    回傳該類別名稱 (str)
    提示：groupby('category')['amount'].sum()
    """
    return df.groupby('category')['amount'].sum().sort_values(ascending=False).index[0] #idxmax()



def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    提示：df[df['vip_level'] == 'Gold']
    """
    return (df[df["vip_level"] == "Gold"].shape[0], df[df["vip_level"] == "Gold"]["amount"].sum())



def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
    提示：groupby('region')['amount'].mean()
    """
    return df.groupby('region')['amount'].mean()


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

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    r =  df.groupby("customer_id")["order_date"].max()
    f = df.groupby("customer_id")["order_id"].count()
    m = df.groupby("customer_id")["amount"].sum()
    names = df.groupby("customer_id")["customer_name"].first()
    df2 = pd.DataFrame({"customer_name":names, "R":r, "F":f, "M":m}).reset_index()

    # df2 = df.groupby("customer_id").agg(customer_name=("customer_name", "first"), R=("order_date", "max"),  F=("order_id", "count"),  M=("amount", "sum")).reset_index()

    return df2.sort_values("M", ascending=False).head(5)

