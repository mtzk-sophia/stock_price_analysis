import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd

def plot_candlestick_with_indicators(df: pd.DataFrame, title: str = "株価チャート"):
    """
    ローソク足チャートとテクニカル指標をプロットする
    
    Args:
        df (pd.DataFrame): 株価データ
        title (str): グラフのタイトル
    """
    # ローソク足チャートの設定
    mc = mpf.make_marketcolors(
        up='red',
        down='blue',
        edge='inherit',
        wick='inherit',
        volume='in',
        ohlc='inherit'
    )
    
    s = mpf.make_mpf_style(
        marketcolors=mc,
        gridstyle='dotted',
        y_on_right=False
    )
    
    # プロットする指標の設定
    apds = [
        mpf.make_addplot(df['SMA_5'], color='blue', width=0.7),
        mpf.make_addplot(df['SMA_25'], color='green', width=0.7),
        mpf.make_addplot(df['SMA_75'], color='red', width=0.7),
        mpf.make_addplot(df['BB_Upper'], color='gray', width=0.7),
        mpf.make_addplot(df['BB_Lower'], color='gray', width=0.7),
    ]
    
    # ローソク足チャートのプロット
    fig, axes = mpf.plot(
        df,
        type='candle',
        style=s,
        title=title,
        addplot=apds,
        volume=True,
        figsize=(15, 10),
        returnfig=True
    )
    
    # RSIのプロット
    fig2, ax2 = plt.subplots(figsize=(15, 3))
    ax2.plot(df.index, df['RSI'], color='purple')
    ax2.axhline(y=70, color='r', linestyle='--')
    ax2.axhline(y=30, color='g', linestyle='--')
    ax2.set_title('RSI')
    ax2.grid(True)
    
    # MACDのプロット
    fig3, ax3 = plt.subplots(figsize=(15, 3))
    ax3.plot(df.index, df['MACD'], color='blue', label='MACD')
    ax3.plot(df.index, df['MACD_Signal'], color='red', label='Signal')
    ax3.bar(df.index, df['MACD_Hist'], color='gray', alpha=0.5)
    ax3.set_title('MACD')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show() 