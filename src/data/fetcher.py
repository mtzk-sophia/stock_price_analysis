import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    指定された銘柄の株価データを取得する
    
    Args:
        symbol (str): 株価コード（例：'7203.T'）
        period (str): 取得期間（例：'1y', '6mo', '1mo'）
    
    Returns:
        pd.DataFrame: 株価データ
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")
        return pd.DataFrame()

def fetch_stock_data_with_dates(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    指定された期間の株価データを取得する
    
    Args:
        symbol (str): 株価コード（例：'7203.T'）
        start_date (str): 開始日（YYYY-MM-DD形式）
        end_date (str): 終了日（YYYY-MM-DD形式）
    
    Returns:
        pd.DataFrame: 株価データ
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)
        return df
    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")
        return pd.DataFrame() 