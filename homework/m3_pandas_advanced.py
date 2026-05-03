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
    df1 = pd.read_csv("datasets/ecommerce/orders_clean.csv")
    df2 = pd.read_csv("datasets/ecommerce/customers.csv")
    df3 = pd.read_csv("datasets/ecommerce/products.csv")
    df4 = pd.merge(df1, df2, on = "customer_id", how = 'left')
    df5 = pd.merge(df4, df3, on = "product_id", how = 'left')#要注意merge有方向性，以誰為主體，誰並過去
    return df5
    pass


def green_row_count(df):
    """回傳 DataFrame 的列數 (int)"""
    # TODO: 你的程式碼
    return len(df)
    pass


def green_column_list(df):
    """回傳 DataFrame 的所有欄位名稱 (list)"""
    # TODO: 你的程式碼
    return list(df.columns)
    pass


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
    price = df.groupby('category')['amount'].sum()
     # idxmax()找最大值
    return price.idmax()
    
    
    


def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    提示：df[df['vip_level'] == 'Gold']
    """
    # TODO: 你的程式碼
    gold_df = df[df['vip_level'] == 'Gold']
    total_order = len(gold_df)
    total_amount = gold_df['amount'].sum()
    return (total_order, total_amount)


def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
    提示：groupby('region')['amount'].mean()
    """
    # TODO: 你的程式碼
    reg = df.groupby('region')['amount'].mean()
    return reg
    
    


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
    rfm_dic = df.groupby("customer_id").agg({
        "order_date":"max", #R 這裡的max是方法
        "customer_id":"count",#F
        "amount" :"sum"#M
    })

    # 改欄位名稱
    rfm_dic.columns = ["R","F","M"]

    # 去看有沒有重複的人，清一清
    name = df[["customer_id","customer_name"]].drop_duplicates()
    # left join 因為有訂單(rfm)的人才把名字算進來
    rfm_dic = rfm_dic.reset_index().merge(name, on = "customer_id", how = "left")
    # 改欄位順序 df[[xxx,xx,x]]
    rfm_dic = rfm_dic[["customer_id", "customer_name", "R", "F", "M"]]
    # 按 M 由大到小排序，要用sort_values，是df有欄位名稱所以可以指定
    rfm_dic = rfm_dic.sort_values("M", ascending = False).head(5)

    return rfm_dic

    
