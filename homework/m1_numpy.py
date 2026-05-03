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
    # TODO:
    arr = np.array([10, 20, 30, 40, 50])
    return arr.mean()
print(green_mean())


def green_double():
    """建立 [10, 20, 30, 40, 50]，回傳所有元素乘以 2 的 ndarray"""
    # TODO: 
    arr = np.array([10, 20, 30, 40, 50])
    return arr * 2
print(green_double())


def green_filter():
    """建立 [10, 20, 30, 40, 50]，回傳大於 25 的元素 (ndarray)"""
    # TODO: 
    arr = np.array([10, 20, 30, 40, 50])
    return arr[arr > 25]
print(green_filter())


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# 以下函式會接收從 products.csv 讀出的 prices, stocks 陣列
# ============================================================
DATA = 'datasets/ecommerce/products.csv'
prices = np.genfromtxt(DATA, delimiter=',', skip_header=1 , usecols=3)
stocks = np.genfromtxt(DATA,delimiter=',', skip_header=1, usecols=4)

def yellow_expensive_count(prices):
    """回傳單價 > 1000 的商品數量 (int)"""
    # TODO:
    return len(prices[prices > 1000])

print(yellow_expensive_count(prices))

def yellow_top3_stock_indices(stocks):
    """
    回傳庫存最多的前 3 個商品的索引位置 (ndarray, 由大到小排)
    提示：np.argsort
    """
    # TODO:
    idx = np.argsort(stocks)
    top3_stocks = idx [-3:][::-1]
    return top3_stocks

print(yellow_top3_stock_indices(stocks))
    


def yellow_restock_cost(prices, stocks):
    """
    單價 < 500 的商品，每種各進貨 50 個，回傳總花費 (float/int)
    提示：布林遮罩 + .sum()
    """
    # TODO:
    mask = prices < 500
    price_500 = prices[mask]
    total_500 = (price_500 * 50).sum()
    return total_500

print(yellow_restock_cost(prices, stocks))

# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_double11_prices(prices, stocks):
    """
    雙 11 定價規則（必須向量化，不能用 for-loop）：
    - 庫存 >= 100：打 7 折
    - 庫存 20~99：打 9 折
    - 庫存 < 20：原價
    回傳每個商品的雙 11 售價 (ndarray)
    提示：np.where 可以巢狀使用
    """
    # TODO:
    prices_07 = prices[stocks >= 100]* 0.7
    prices_09 = prices[(stocks >= 20) & (stocks <= 99)] * 0.9
    prices_original = prices[stocks < 20]

    finall_price = np.concatenate([prices_07, prices_09, prices_original])
    
    #運用np.where取代if-else的方式
    finall_price2 = np.where(stocks >= 100, prices * 0.7,#庫存大於100 ,true:價格x0.7
                             np.where(stocks >= 20,prices * 0.9 ,prices))#庫存 >= 20 ,true:價格x0.9,庫存 < 20,false:價格原價
    return finall_price2