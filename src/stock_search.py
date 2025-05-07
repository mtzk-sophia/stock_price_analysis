#%%
from data.stock_list import get_japanese_stock_list, search_stocks, get_stock_info
import pandas as pd

#%%
# 全上場企業一覧を取得
df = get_japanese_stock_list()
print(f"上場企業数: {len(df)}")
df.head()

#%%
df['market'].unique()
#%%
# キーワードで企業を検索
keyword = "トヨタ"  # 検索キーワードを変更可能
results = search_stocks(keyword)
print(f"検索結果: {len(results)}件")
results

#%%
# 特定の銘柄の詳細情報を取得
symbol = "7203.T"  # トヨタ自動車
info = get_stock_info(symbol)
pd.Series(info) 
# %%
