"""
M2 Pandas I/O 與資料清理 — 課後作業
====================================
情境：你拿到一份「故意弄髒」的訂單 CSV (orders_raw.csv)，
裡面有欄位名稱空格、金額帶 $ 符號、日期格式錯誤、缺值、重複列。
請用 Pandas 把它清乾淨。

資料路徑：datasets/ecommerce/orders_raw.csv
"""
import pandas as pd

# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_read_csv():
    """讀取 orders_raw.csv，回傳原始 DataFrame"""
    df = pd.read_csv('datasets/ecommerce/orders_raw.csv')
    return df


def green_shape(df):
    """回傳 DataFrame 的 (列數, 欄數) tuple"""
    return df.shape


def green_dtypes(df):
    """回傳 DataFrame 的欄位型別 (Series)"""
    return df.dtypes


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_columns(df):
    """清理欄位名稱：去除前後空白、全部轉小寫"""
    new_df = df.copy()
    new_df.columns = new_df.columns.str.strip().str.lower()
    return new_df


def yellow_clean_amount(df):
    """清理 amount 欄位：移除 '$' 和 ',' 符號，轉為 float"""
    new_df = df.copy()
    # 先將符號取代為空字串，再轉換型別
    new_df['amount'] = new_df['amount'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
    return new_df


def yellow_drop_duplicates(df):
    """移除完全重複的列"""
    return df.drop_duplicates()


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_clean_orders(path):
    """完整清理 pipeline"""
    # 1. 讀取 CSV
    df = pd.read_csv(path)
    
    # 2. 欄位名稱：去空白、轉小寫
    df.columns = df.columns.str.strip().str.lower()
    
    # 3. amount：移除 '$' ','，轉 float
    # 使用 regex=True 的一次性取代或連續 replace
    df['amount'] = df['amount'].str.replace(r'[\$,]', '', regex=True).astype(float)
    
    # 4. order_date：轉為 datetime（無法轉換的設為 NaT）
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    
    # 5. 刪除 amount 或 order_date 為空的列
    df = df.dropna(subset=['amount', 'order_date'])
    
    # 6. 移除重複列
    df = df.drop_duplicates()

    return df
