import pandas as pd
import ta

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    株価データにテクニカル指標を追加する
    
    Args:
        df (pd.DataFrame): 株価データ
    
    Returns:
        pd.DataFrame: テクニカル指標を追加した株価データ
    """
    # 移動平均
    df['SMA_5'] = ta.trend.sma_indicator(df['Close'], window=5)
    df['SMA_25'] = ta.trend.sma_indicator(df['Close'], window=25)
    df['SMA_75'] = ta.trend.sma_indicator(df['Close'], window=75)
    
    # RSI
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Hist'] = macd.macd_diff()
    
    # ボリンジャーバンド
    bollinger = ta.volatility.BollingerBands(df['Close'])
    df['BB_Upper'] = bollinger.bollinger_hband()
    df['BB_Lower'] = bollinger.bollinger_lband()
    df['BB_Middle'] = bollinger.bollinger_mavg()
    
    return df 