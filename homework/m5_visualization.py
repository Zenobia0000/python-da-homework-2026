"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import matplotlib
matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================
class Green:
    def green_bar_category():
        """
        畫出每個商品類別 (category) 的訂單數長條圖
        回傳 matplotlib Figure 物件
        提示：sns.countplot 或 value_counts().plot.bar()
        """
        # TODO: 你的程式碼
        df = _load_data()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='category', order=df['category'].value_counts().index, ax=ax)
        ax.set_title('Orders by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Order Count')
        plt.tight_layout()
        return fig


    def green_hist_amount():
        """
        畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
        回傳 matplotlib Figure 物件
        提示：sns.histplot(bins=20) 或 plt.hist()
        """
        # TODO: 你的程式碼
        df = _load_data()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df, x='amount', bins=20, ax=ax)
        ax.set_title('Order Amount Distribution')
        ax.set_xlabel('Amount')
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        return fig


    def green_set_labels():
        """
        建立一個簡單的長條圖（內容不限），但必須設定：
        - 圖標題 (title)
        - X 軸標籤 (xlabel)
        - Y 軸標籤 (ylabel)
        回傳 matplotlib Figure 物件
        """
        # TODO: 你的程式碼
        df = _load_data()
        fig, ax = plt.subplots(figsize=(8, 5))
        df['category'].value_counts().plot.bar(ax=ax)
        ax.set_title('Orders by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Order Count')
        plt.tight_layout()
        return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================
class Yellow:
    def yellow_line_region_trend():
        """
        畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
        - X 軸：月份
        - Y 軸：該月總營收
        - 兩條線，有圖例 (legend)
        回傳 matplotlib Figure 物件
        提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
        """
        # TODO: 你的程式碼
        df = _load_data()
        df['month'] = df['order_date'].dt.to_period('M')
        
        filtered = df[df['region'].isin(['North', 'South'])]
        monthly = (
            filtered.groupby(['month', 'region'])['amount']
            .sum()
            .reset_index()
        )
        monthly['month'] = monthly['month'].dt.to_timestamp()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=monthly, x='month', y='amount', hue='region', ax=ax)
        ax.set_title('Monthly Revenue: North vs South')
        ax.set_xlabel('Month')
        ax.set_ylabel('Revenue')
        plt.tight_layout()
        return fig


    def yellow_box_vip():
        """
        畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
        回傳 matplotlib Figure 物件
        提示：sns.boxplot(x='vip_level', y='amount', data=df)
        """
        # TODO: 你的程式碼
        df = _load_data()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, x='vip_level', y='amount', ax=ax)
        ax.set_title('Order Amount by VIP Level')
        ax.set_xlabel('VIP Level')
        ax.set_ylabel('Amount')
        plt.tight_layout()
        return fig


    def yellow_scatter_price_amount():
        """
        畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
        回傳 matplotlib Figure 物件
        提示：plt.scatter() 或 sns.scatterplot()
        """
        # TODO: 你的程式碼
        df = _load_data()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df, x='unit_price', y='amount', alpha=0.5, ax=ax)
        ax.set_title('Unit Price vs Order Amount')
        ax.set_xlabel('Unit Price')
        ax.set_ylabel('Amount')
        plt.tight_layout()
        return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================
class Red:
    def red_category_dashboard(category="Electronics"):
        """
        針對指定類別，畫 2×2 的 subplot dashboard：
        1. 左上：該類別月營收趨勢 (折線圖)
        2. 右上：該類別各地區營收 (長條圖)
        3. 左下：該類別 Top 5 商品營收 (水平長條圖)
        4. 右下：該類別訂單金額分佈 (直方圖)

        回傳 matplotlib Figure 物件
        提示：fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        """
        # TODO: 你的程式碼
        df = _load_data()
        cat_df = df[df['category'] == category].copy()
        cat_df['month'] = cat_df['order_date'].dt.to_period('M')

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'{category} Dashboard', fontsize=16, fontweight='bold')

        monthly_rev = cat_df.groupby('month')['amount'].sum()
        monthly_rev.index = monthly_rev.index.to_timestamp()
        axes[0, 0].plot(monthly_rev.index, monthly_rev.values, marker='o')
        axes[0, 0].set_title('Monthly Revenue Trend')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Revenue')

        region_rev = cat_df.groupby('region')['amount'].sum().sort_values(ascending=False)
        axes[0, 1].bar(region_rev.index, region_rev.values)
        axes[0, 1].set_title('Revenue by Region')
        axes[0, 1].set_xlabel('Region')
        axes[0, 1].set_ylabel('Revenue')

        top5 = (
            cat_df.groupby('product_name')['amount']
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        axes[1, 0].barh(top5.index[::-1], top5.values[::-1])
        axes[1, 0].set_title('Top 5 Products by Revenue')
        axes[1, 0].set_xlabel('Revenue')
        axes[1, 0].set_ylabel('Product')

        axes[1, 1].hist(cat_df['amount'], bins=20, edgecolor='white')
        axes[1, 1].set_title('Order Amount Distribution')
        axes[1, 1].set_xlabel('Amount')
        axes[1, 1].set_ylabel('Frequency')

        plt.tight_layout()
        return fig
