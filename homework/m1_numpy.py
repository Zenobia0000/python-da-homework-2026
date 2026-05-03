"""
M1 NumPy 向量化思維 — 課後作業
================================
請完成以下每個函式，用 NumPy 向量化寫法（不要 for-loop）。
完成後 git push，GitHub Actions 會自動批改並顯示成績與解答。

提示：
- np.array, np.where, np.argsort
- 布林遮罩: arr[arr > 10]
- 統計: .sum(), .mean(), .max(), .min()
"""
import numpy as np


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_mean():
    """建立 [10, 20, 30, 40, 50]，回傳所有元素的平均值 (float)"""
    arr = np.array([10,20,30,40,50]) 
    return arr.mean()
print(green_mean())
    

def green_double():
    """建立 [10, 20, 30, 40, 50]，回傳所有元素乘以 2 的 ndarray"""
    arr = np.array([10,20,30,40,50])
    return arr*2
print(green_double())

def green_filter():
    """建立 [10, 20, 30, 40, 50]，回傳大於 25 的元素 (ndarray)"""
    arr = np.array([10,20,30,40,50])
    result = arr[arr>25]
    return result
print(green_filter())

# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# 以下函式會接收從 products.csv 讀出的 prices, stocks 陣列
# ============================================================

def yellow_expensive_count(prices):
    """回傳單價 > 1000 的商品數量 (int)"""
    prices_arr = np.array(prices)
    gold = prices_arr[prices_arr>1000]
    
    return gold

test_prices = [500, 1200, 800, 2500, 100]
test_prices = len(yellow_expensive_count(test_prices))
print(test_prices)



def yellow_top3_stock_indices(stocks):
    arr = np.array(stocks)
    indices = np.argsort(arr)[::-1][:3]
    top3_values = arr[indices]
    return  top3_values
list = [100,200,300,400,500]
print(yellow_top3_stock_indices(list))    
    

# """
# 回傳庫存最多的前 3 個商品的索引位置 (ndarray, 由大到小排)
# 提示：np.argsort
# """
    


# def yellow_restock_cost(prices, stocks):
# """
# 單價 < 500 的商品，每種各進貨 50 個，回傳總花費 (float/int)
# 提示：布林遮罩 + .sum()
# """
    # TODO: 你的程式碼
# pass


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

# def red_double11_prices(prices, stocks):
#     """
#     雙 11 定價規則（必須向量化，不能用 for-loop）：
#     - 庫存 >= 100：打 7 折
#     - 庫存 20~99：打 9 折
#     - 庫存 < 20：原價
#     回傳每個商品的雙 11 售價 (ndarray)
#     提示：np.where 可以巢狀使用
#     """
#     # TODO: 你的程式碼
#     pass
