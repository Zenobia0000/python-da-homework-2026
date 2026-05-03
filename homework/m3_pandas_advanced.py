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
    """
    path_prefix = r"C:\Users\W11 HOME\Desktop\python-da-homework-2026\datasets\ecommerce/"
    
    # 讀取資料
    df_orders = pd.read_csv(path_prefix + "orders_clean.csv")
    df_customers = pd.read_csv(path_prefix + "customers.csv")
    df_products = pd.read_csv(path_prefix + "products.csv")
    
    # 轉換日期格式 (確保 RFM 計算正常)
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    
    # 合併：先併客戶，再併產品
    merged_df = pd.merge(df_orders, df_customers, on='customer_id', how='left')
    final_df = pd.merge(merged_df, df_products, on='product_id', how='left')
    
    return final_df

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
    回傳該類別名稱 (str)
    """
    return df.groupby('category')['amount'].sum().idxmax()


def yellow_gold_vip_stats(df):
    """
    Gold VIP 客戶總共下了幾張訂單？總金額多少？
    回傳 tuple: (訂單數 int, 總金額 float)
    """
    gold_df = df[df['vip_level'] == 'Gold']
    order_count = len(gold_df)
    total_amount = gold_df['amount'].sum()
    return (order_count, float(total_amount))


def yellow_region_avg_amount(df):
    """
    計算每個地區 (region) 的平均訂單金額
    回傳 Series（index=region, values=平均金額）
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
    """
    # 聚合計算 RFM
    rfm = df.groupby(['customer_id', 'customer_name']).agg(
        R=('order_date', 'max'),
        F=('order_id', 'count'),
        M=('amount', 'sum')
    ).reset_index()
    
    # 按 M (Monetary) 由大到小排序，取前 5 筆
    return rfm.sort_values('M', ascending=False).head(5)

# ============================================================
# 🏁 測試與驗收區
# ============================================================
if __name__ == "__main__":
    try:
        main_df = green_load_and_merge()
        print(f"✅ 成功載入 {green_row_count(main_df)} 筆資料")
        print(f"📊 營收最高類別：{yellow_top_category(main_df)}")
        
        vip_count, vip_sum = yellow_gold_vip_stats(main_df)
        print(f"💎 Gold VIP：共 {vip_count} 筆訂單，總計 ${vip_sum:,.0f}")
        
        print("\n🏆 RFM 最有價值客戶 Top 5：")
        print(red_rfm_top5(main_df))
    except Exception as e:
        print(f"❌ 執行出錯：{e}")