import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시총 Top 10 기업 주가 변화")

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
    """지정된 티커의 주식 데이터를 가져옵니다."""
    try:
        data = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)

        if data.empty:
            # st.warning(f"티커 '{ticker_symbol}'에 대한 {start_date.strftime('%Y-%m-%d')}부터 {end_date.strftime('%Y-%m-%d')}까지의 주식 데이터를 찾을 수 없습니다.")
            return None
        
        # 'Adj Close' 컬럼이 있으면 사용, 없으면 'Close' 컬럼을 사용합니다.
        # 캔들스틱 차트도 이 데이터를 사용하므로, 필요한 컬럼들이 존재하는지 확인해야 합니다.
        if 'Adj Close' in data.columns and not data['Adj Close'].empty:
            data['Price'] = data['Adj Close'] # 통합된 'Price' 컬럼 생성
        elif 'Close' in data.columns and not data['Close'].empty:
            data['Price'] = data['Close'] # 통합된 'Price' 컬럼 생성
        else:
            # st.error(f"티커 '{ticker_symbol}'의 데이터에 'Adj Close' 또는 'Close' 컬럼이 없습니다.")
            return None # Price 컬럼을 만들 수 없으면 None 반환

        return data[['Open', 'High', 'Low', 'Close', 'Price']] # 캔들스틱에 필요한 컬럼과 Price 컬럼 반환

    except Exception as e:
        # st.error(f"티커 '{ticker_symbol}'의 데이터를 가져오는 중 예상치 못한 오류 발생: {e}")
        return None

# 날짜 설정
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 3년 전

st.write(f"기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

# --- 희망 기업 선택 기능 추가 ---
st.sidebar.header("기업 선택")
selected_companies_names = st.sidebar.multiselect(
    "주가 변화를 보고 싶은 기업을 선택하세요:",
    options=list(TOP_10_COMPANIES.values()),
    default=list(TOP_10_COMPANIES.values()) # 기본적으로 모든 기업 선택
)

# 선택된 기업의 티커 리스트 생성
selected_tickers = {ticker: name for ticker, name in TOP_10_COMPANIES.items() if name in selected_companies_names}
# --- 희망 기업 선택 기능 끝 ---

# 모든 기업의 데이터 가져오기
all_stock_data_raw = {} # 개별 기업의 상세 데이터(Open, High, Low, Close, Price)를 저장
all_price_data = pd.DataFrame() # 정규화된 가격 데이터(Price)만 저장

st.subheader("주식 데이터 가져오기 진행 중...")
progress_bar_placeholder = st.empty()
progress_bar = progress_bar_placeholder.progress(0)
message_placeholder = st.empty()

# 선택된 기업만 데이터를 가져옵니다.
for i, (ticker, name) in enumerate(selected_tickers.items()):
    message_placeholder.text(f"데이터 가져오는 중: {name} ({ticker})...")
    
    # get_stock_data 함수는 필요한 모든 컬럼을 포함하는 DataFrame을 반환합니다.
    data_df = get_stock_data(ticker, start_date, end_date)
    
    if data_df is not None and not data_df.empty:
        all_stock_data_raw[name] = data_df
        if 'Price' in data_df.columns:
            all_price_data[name] = data_df['Price']
    progress_bar.progress((i + 1) / len(selected_tickers)) # 선택된 기업 수에 따라 진행률 업데이트

message_placeholder.empty()
progress_bar_placeholder.empty()

if not all_price_data.empty:
    # 초기 가격을 100으로 정규화하여 변화율 비교
    # 모든 컬럼이 NaN인 경우를 대비하여 NaN 처리 후 정규화
    normalized_data = all_price_data.dropna(axis=1, how='all') # 모든 값이 NaN인 컬럼 제거
    if not normalized_data.empty:
        normalized_data = normalized_data / normalized_data.iloc[0] * 100

        st.subheader("기간별 주가 변화 (초기 가격 100으로 정규화)")

        fig = go.Figure()
        for col in normalized_data.columns:
            fig.add_trace(go.Scatter(x=normalized_data.index, y=normalized_data[col], mode='lines', name=col))

        fig.update_layout(
            title="선택된 글로벌 시총 Top 기업 주가 변화",
            xaxis_title="날짜",
            yaxis_title="정규화된 주가 (시작점 100)",
            hovermode="x unified",
            legend_title="기업",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("정규화할 유효한 주식 데이터가 없습니다. 선택된 기업의 데이터를 확인해주세요.")

else:
    st.error("데이터를 가져오는 데 실패했거나, 선택된 기업의 데이터가 없습니다. 티커 목록을 확인하거나 잠시 후 다시 시도해 주세요.")

st.markdown("---")
st.subheader("개별 기업 주가 상세 보기 (캔들스틱 차트)")

# 데이터가 성공적으로 로드된 기업만 선택 옵션에 포함
available_for_candlestick = list(all_stock_data_raw.keys())
    
if available_for_candlestick:
    selected_company_for_candlestick = st.selectbox(
        "캔들스틱 차트를 보고 싶은 기업을 선택하세요:",
        options=available_for_candlestick
    )

    if selected_company_for_candlestick:
        ticker_symbol_for_candlestick = [k for k, v in TOP_10_COMPANIES.items() if v == selected_company_for_candlestick][0]
        
        st.write(f"**{selected_company_for_candlestick} ({ticker_symbol_for_candlestick})**")
        
        candlestick_data = all_stock_data_raw.get(selected_company_for_candlestick) # 캐시된 데이터 사용

        if candlestick_data is not None and not candlestick_data.empty:
            # 캔들스틱 차트에 필요한 컬럼들이 모두 있는지 확인
            required_cols = ['Open', 'High', 'Low', 'Close']
            if all(col in candlestick_data.columns for col in required_cols):
                fig_candlestick = go.Figure(data=[go.Candlestick(
                    x=candlestick_data.index,
                    open=candlestick_data['Open'],
                    high=candlestick_data['High'],
                    low=candlestick_data['Low'],
                    close=candlestick_data['Close']
                )])

                fig_candlestick.update_layout(
                    title=f"{selected_company_for_candlestick} 캔들스틱 차트",
                    xaxis_title="날짜",
                    yaxis_title="주가",
                    xaxis_rangeslider_visible=False,
                    height=500
                )
                st.plotly_chart(fig_candlestick, use_container_width=True)
            else:
                st.warning(f"{selected_company_for_candlestick} 의 캔들스틱 차트를 그리는 데 필요한 데이터(Open, High, Low, Close)가 불완전합니다.")
        else:
            st.warning(f"{selected_company_for_candlestick} 의 캔들스틱 차트 데이터를 가져올 수 없습니다. 다시 시도하거나 다른 기업을 선택하세요.")

else:
    st.info("선택된 기업 중 주식 데이터를 성공적으로 가져온 기업이 없습니다. 캔들스틱 차트를 표시할 수 없습니다.")

st.markdown("---")
st.info("데이터는 Yahoo Finance에서 가져오며, 지연될 수 있습니다. 시가총액 상위 기업 목록은 시간에 따라 변경될 수 있으므로, 최신 정보를 반영하려면 `TOP_10_COMPANIES` 딕셔너리를 업데이트해야 합니다.")
