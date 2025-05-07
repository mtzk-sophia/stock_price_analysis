import os

import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import time

def get_japanese_stock_list():
    """
    日本企業の株価コード一覧を取得する
    
    Returns:
        pd.DataFrame: 企業コード、企業名、市場区分を含むDataFrame
    """
    # 現在のファイルのディレクトリを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # プロジェクトのルートディレクトリを取得（srcの親ディレクトリ）
    project_root = os.path.dirname(os.path.dirname(current_dir))
    # Excelファイルのパスを構築
    excel_path = os.path.join(project_root, 'data', 'raw', 'data_j.xls')
    
    # Excelファイルから企業情報を読み込む
    df = pd.read_excel(excel_path)
    
    # 必要な列を選択し、列名を統一
    df = df[['コード', '銘柄名', '市場・商品区分', '33業種区分', '17業種区分']]
    df.columns = ['code', 'name', 'market', 'industry_33', 'industry_17']
    
    # 企業コードをYahoo Finance形式に変換（例：7203 → 7203.T）
    df['yahoo_code'] = df['code'].astype(str).str.zfill(4) + '.T'
    
    return df

def search_stocks(keyword: str) -> pd.DataFrame:
    """
    キーワードで企業を検索する
    
    Args:
        keyword (str): 検索キーワード（企業名やコード）
    
    Returns:
        pd.DataFrame: 検索結果
    """
    df = get_japanese_stock_list()
    # 企業名とコードで検索
    mask = (df['name'].str.contains(keyword, case=False) | 
            df['code'].str.contains(keyword, case=False))
    return df[mask]

def get_stock_info(symbol: str) -> dict:
    """
    指定された銘柄の基本情報を取得する
    
    Args:
        symbol (str): 株価コード（例：'7203.T'）
    
    Returns:
        dict: 企業情報
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        return {
            'symbol': symbol,
            'name': info.get('longName', '不明'),
            'sector': info.get('sector', '不明'),
            'industry': info.get('industry', '不明'),
            'market_cap': info.get('marketCap', '不明'),
            'currency': info.get('currency', 'JPY')
        }
    except Exception as e:
        print(f"情報取得中にエラーが発生しました: {e}")
        return {} 