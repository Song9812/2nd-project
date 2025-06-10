import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시총 Top 10 기업 주가 변화 (최근 3년)")

TOP_10_COMPANIES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet (Google) A",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "META": "Meta Platforms",
    "TSLA": "Tesla",
    "BRK-A": "Berkshire Hathaway A",
    "JPM": "JPMorgan Chase",
    "LLY": "Eli Lilly and Company",
}

@st.cache_data
def get_stock_data(ticker_symbol, start_date, end_date):
    """지정된 티커의 주식 데이터를 가져옵니다. 'Adj Close' 대신 'Close'를 기본으로 사용합니다."""
    try:
        data = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)

        if data.empty:
            st.warning(f"티커 '{ticker_symbol}'에 대한 {start_date.strftime('%Y-%m-%d')}부터 {end_date.strftime('%Y-%m-%d')}까지의 주식 데이터를 찾을 수 없습니다.")
            return None
        
        # 'Adj Close' 컬럼이 있으면 사용, 없으면 'Close' 컬럼을 사용합니다.
        # 이전처럼 경고 메시지는 출력하지 않습니다.
        if 'Adj Close' in data.columns:
            return data['Adj Close']
        elif 'Close' in data.columns:
            return data['Close']
        else:
            st.error(f"티커 '{ticker_symbol}'의 데이터에 'Adj Close' 또는 'Close' 컬럼이 없습니다.")
            return None

    except Exception as e:
        st.error(f"티커 '{ticker_symbol}'의 데이터를 가져오는 중 예상치 못한 오류 발생: {e}")
        return None

# 날짜 설정
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 3년 전

st.write(f"기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

# 모든 기업의 데이터 가져오기
all_stock_data = pd.DataFrame()
st.subheader("주식 데이터 가져오기 진행 중...")
progress_bar_placeholder = st.empty()
progress_bar = progress_bar_placeholder.progress(0)

# 메시지를 위한 placeholder
message_placeholder = st.empty()


for i, (ticker, name) in enumerate(TOP_10_COMPANIES.items()):
    message_placeholder.text(f"데이터 가져오는 중: {name} ({ticker})...")
    data_series = get_stock_data(ticker, start_date, end_date)
    if data_series is not None:
        all_stock_data[name] = data_series
    progress_bar.progress((i + 1) / len(TOP_10_COMPANIES))

message_placeholder.empty() # 모든 데이터 로드 후 메시지 제거
progress_bar_placeholder.empty() # 모든 데이터 로드 후 진행 바 제거


if not all_stock_data.empty:
    # 초기 가격을 100으로 정규화하여 변화율 비교
    # 모든 컬럼이 NaN인 경우를 대비하여 NaN 처리 후 정규화
    normalized_data = all_stock_data.dropna(axis=1, how='all') # 모든 값이 NaN인 컬럼 제거
    if not normalized_data.empty:
        normalized_data = normalized_data / normalized_data.iloc[0] * 100

        st.subheader("기간별 주가 변화 (초기 가격 100으로 정규화)")

        fig = go.Figure()
        for col in normalized_data.columns:
            fig.add_trace(go.Scatter(x=normalized_data.index, y=normalized_data[col], mode='lines', name=col))

        fig.update_layout(
            title="글로벌 시총 Top 10 기업 주가 변화",
            xaxis_title="날짜",
            yaxis_title="정규화된 주가 (시작점 100)",
            hovermode="x unified",
            legend_title="기업",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("정규화할 유효한 주식 데이터가 없습니다.")

    st.markdown("---")
    st.subheader("개별 기업 주가 상세 보기")

    # 데이터가 성공적으로 로드된 기업만 선택 옵션에 포함
    available_companies = [name for name in TOP_10_COMPANIES.values() if name in all_stock_data.columns]
    
    if available_companies:
        selected_company = st.selectbox(
            "기업을 선택하세요:",
            options=available_companies
        )

        if selected_company:
            # 선택된 기업의 티커 심볼 찾기
            ticker_symbol = [k for k, v in TOP_10_COMPANIES.items() if v == selected_company][0]
            
            st.write(f"**{selected_company} ({ticker_symbol})**")
            
            # 캔들스틱 차트 그리기
            candlestick_data = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)
            
            if not candlestick_data.empty:
                fig_candlestick = go.Figure(data=[go.Candlestick(
                    x=candlestick_data.index,
                    open=candlestick_data['Open'],
                    high=candlestick_data['High'],
                    low=candlestick_data['Low'],
                    close=candlestick_data['Close']
                )])

                fig_candlestick.update_layout(
                    title=f"{selected_company} 캔들스틱 차트",
                    xaxis_title="날짜",
                    yaxis_title="주가",
                    xaxis_rangeslider_visible=False,
                    height=500
                )
                st.plotly_chart(fig_candlestick, use_container_width=True)
            else:
                st.warning(f"{selected_company} 의 캔들스틱 차트 데이터를 가져올 수 없습니다.")
    else:
        st.warning("주식 데이터를 성공적으로 가져온 기업이 없습니다. 선택할 기업이 없습니다.")

else:
    st.error("데이터를 가져오는 데 실패했습니다. 티커 목록을 확인하거나 잠시 후 다시 시도해 주세요.")

st.markdown("---")
st.info("데이터는 Yahoo Finance에서 가져오며, 지연될 수 있습니다. 시가총액 상위 기업 목록은 시간에 따라 변경될 수 있으므로, 최신 정보를 반영하려면 `TOP_10_COMPANIES` 딕셔너리를 업데이트해야 합니다.")
