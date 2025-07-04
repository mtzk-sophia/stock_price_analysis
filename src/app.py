import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data.fetcher import fetch_stock_data
from data.processor import add_technical_indicators
from data.stock_list import get_japanese_stock_list, search_stocks
import jpholiday
from datetime import datetime, timedelta

def remove_holidays(df: pd.DataFrame) -> pd.DataFrame:
    """
    土日祝日を除外したデータフレームを返す
    
    Args:
        df (pd.DataFrame): 元のデータフレーム
    
    Returns:
        pd.DataFrame: 土日祝日を除外したデータフレーム
    """
    # 土日祝日を除外
    business_days = []
    for date in df.index:
        # 土曜日(5)と日曜日(6)を除外
        if date.weekday() >= 5:
            continue
        # 祝日を除外
        if jpholiday.is_holiday(date):
            continue
        business_days.append(date)
    
    # 土日祝日を除外したデータフレームを作成
    return df.loc[business_days].copy()

def plot_candlestick_with_indicators_streamlit(df: pd.DataFrame, title: str = "株価チャート"):
    """
    Streamlit用にローソク足チャートとテクニカル指標をPlotlyでプロットする
    
    Args:
        df (pd.DataFrame): 株価データ
        title (str): グラフのタイトル
    """
    # 土日祝日を除外
    df = remove_holidays(df)
    
    # 日付を文字列に変換
    df.index = df.index.strftime('%Y-%m-%d')
    
    # MACDのゴールデンクロスを検出
    golden_cross = (df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1))
    golden_cross_dates = df.index[golden_cross]
    golden_cross_values = df.loc[golden_cross, 'MACD']
    
    # MACDのデッドクロスを検出
    dead_cross = (df['MACD'] < df['MACD_Signal']) & (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1))
    dead_cross_dates = df.index[dead_cross]
    dead_cross_values = df.loc[dead_cross, 'MACD']
    
    # サブプロットの作成
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.2, 0.15, 0.15],
        subplot_titles=(title, '出来高', 'RSI', 'MACD')
    )

    # ローソク足チャート
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='ローソク足',
            hoverinfo='text',
            text=[f'日付: {date}<br>始値: {open:.0f}<br>高値: {high:.0f}<br>安値: {low:.0f}<br>終値: {close:.0f}'
                  for date, open, high, low, close in zip(df.index, df['Open'], df['High'], df['Low'], df['Close'])]
        ),
        row=1, col=1
    )

    # 移動平均線
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['SMA_5'],
            name='SMA5',
            line=dict(color='blue'),
            hoverinfo='text',
            text=[f'日付: {date}<br>SMA5: {y:.0f}' for date, y in zip(df.index, df['SMA_5'])]
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['SMA_25'],
            name='SMA25',
            line=dict(color='green'),
            hoverinfo='text',
            text=[f'日付: {date}<br>SMA25: {y:.0f}' for date, y in zip(df.index, df['SMA_25'])]
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['SMA_75'],
            name='SMA75',
            line=dict(color='red'),
            hoverinfo='text',
            text=[f'日付: {date}<br>SMA75: {y:.0f}' for date, y in zip(df.index, df['SMA_75'])]
        ),
        row=1, col=1
    )

    # ボリンジャーバンド
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['BB_Upper'],
            name='BB Upper',
            line=dict(color='gray', dash='dash'),
            hoverinfo='text',
            text=[f'日付: {date}<br>BB Upper: {y:.0f}' for date, y in zip(df.index, df['BB_Upper'])]
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['BB_Lower'],
            name='BB Lower',
            line=dict(color='gray', dash='dash'),
            hoverinfo='text',
            text=[f'日付: {date}<br>BB Lower: {y:.0f}' for date, y in zip(df.index, df['BB_Lower'])]
        ),
        row=1, col=1
    )

    # 出来高
    colors = ['red' if row['Open'] > row['Close'] else 'blue' for _, row in df.iterrows()]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='出来高',
            marker_color=colors,
            hoverinfo='text',
            text=[f'日付: {date}<br>出来高: {y:,.0f}' for date, y in zip(df.index, df['Volume'])],
            textposition='none'  # 棒グラフ内の数値を非表示
        ),
        row=2, col=1
    )

    # RSI
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['RSI'],
            name='RSI',
            line=dict(color='purple'),
            hoverinfo='text',
            text=[f'日付: {date}<br>RSI: {y:.1f}' for date, y in zip(df.index, df['RSI'])]
        ),
        row=3, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    # MACD
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MACD'],
            name='MACD',
            line=dict(color='blue'),
            hoverinfo='text',
            text=[f'日付: {date}<br>MACD: {y:.1f}' for date, y in zip(df.index, df['MACD'])]
        ),
        row=4, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MACD_Signal'],
            name='Signal',
            line=dict(color='red'),
            hoverinfo='text',
            text=[f'日付: {date}<br>Signal: {y:.1f}' for date, y in zip(df.index, df['MACD_Signal'])]
        ),
        row=4, col=1
    )
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['MACD_Hist'],
            name='Histogram',
            marker_color='gray',
            hoverinfo='text',
            text=[f'日付: {date}<br>Histogram: {y:.1f}' for date, y in zip(df.index, df['MACD_Hist'])],
            textposition='none'  # 棒グラフ内の数値を非表示
        ),
        row=4, col=1
    )

    # ゴールデンクロスのマーカーを追加
    fig.add_trace(
        go.Scatter(
            x=golden_cross_dates,
            y=golden_cross_values,
            mode='markers',
            name='ゴールデンクロス',
            marker=dict(
                symbol='triangle-up',
                size=12,
                color='gold',
                line=dict(color='black', width=1)
            ),
            hoverinfo='text',
            text=[f'ゴールデンクロス<br>日付: {date}<br>MACD: {y:.1f}' 
                  for date, y in zip(golden_cross_dates, golden_cross_values)]
        ),
        row=4, col=1
    )

    # デッドクロスのマーカーを追加
    fig.add_trace(
        go.Scatter(
            x=dead_cross_dates,
            y=dead_cross_values,
            mode='markers',
            name='デッドクロス',
            marker=dict(
                symbol='triangle-down',
                size=12,
                color='lightgreen',
                line=dict(color='black', width=1)
            ),
            hoverinfo='text',
            text=[f'デッドクロス<br>日付: {date}<br>MACD: {y:.1f}' 
                  for date, y in zip(dead_cross_dates, dead_cross_values)]
        ),
        row=4, col=1
    )

    # レイアウトの設定
    fig.update_layout(
        height=1000,
        xaxis_rangeslider_visible=False,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        # 日付表示の設定
        xaxis=dict(
            type='category',
            tickangle=45,
            tickmode='auto',
            nticks=10,
            showgrid=True,
            gridcolor='lightgray',
            rangeslider=dict(visible=False)
        ),
        # マージンの調整
        margin=dict(l=0, r=0, t=50, b=0),
        # ホバー設定
        hovermode='x unified'
    )

    # 各サブプロットのx軸の設定を統一
    for i in range(1, 5):
        fig.update_xaxes(
            type='category',
            tickangle=45,
            tickmode='auto',
            nticks=10,
            showgrid=True,
            gridcolor='lightgray',
            row=i, col=1
        )

    # Streamlitで表示（コンテナ幅いっぱいに表示）
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

def main():
    # ページの設定
    st.set_page_config(
        page_title="株価チャート分析アプリ",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title('株価チャート分析アプリ')
    
    # 3カラムレイアウトで選択肢を横並びに
    col1, col2, col3 = st.columns([2, 2, 1])
    
    # 企業コードのリストを取得
    stock_list = get_japanese_stock_list()
    
    with col1:
        # 33業種区分のリストを取得（重複を除去）
        industries = sorted(stock_list['industry_33'].unique())
        
        # 業種選択
        selected_industry = st.selectbox(
            '業種を選択してください',
            options=industries,
            index=0
        )
    
    with col2:
        # 選択された業種の企業のみをフィルタリング
        filtered_stocks = stock_list[stock_list['industry_33'] == selected_industry]
        
        # 企業コードと企業名の組み合わせを作成
        stock_options = {f"{row['name']} ({row['code']})": row['yahoo_code'] 
                        for _, row in filtered_stocks.iterrows()}
        
        # 企業選択
        selected_stock = st.selectbox(
            '企業を選択してください',
            options=list(stock_options.keys()),
            index=0
        )
        symbol = stock_options[selected_stock]
    
    with col3:
        # 期間選択
        period = st.selectbox(
            '期間を選択してください',
            options=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
            index=2
        )
    
    # データ取得と表示
    if st.button('チャートを表示', use_container_width=True):
        with st.spinner('データを取得中...'):
            df = fetch_stock_data(symbol, period=period)
            df = add_technical_indicators(df)
            plot_candlestick_with_indicators_streamlit(df, title=f"{symbol} 株価チャート")

if __name__ == "__main__":
    main() 