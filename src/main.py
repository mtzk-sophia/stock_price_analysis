# %%
from data.fetcher import fetch_stock_data
from data.processor import add_technical_indicators
from visualization.plotter import plot_candlestick_with_indicators


def main():
    # トヨタ自動車の株価データを取得
    symbol = "7203.T"
    df = fetch_stock_data(symbol, period="6mo")
    
    # テクニカル指標を追加
    df = add_technical_indicators(df)
    
    # チャートをプロット
    plot_candlestick_with_indicators(df, title=f"{symbol} 株価チャート")

if __name__ == "__main__":
    main()
