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
            return None
        
        if 'Adj Close' in data.columns and not data['Adj Close'].empty:
            data['Price'] = data['Adj Close']
        elif 'Close' in data.columns and not data['Close'].empty:
            data['Price'] = data['Close']
        else:
            return None

        # 캔들스틱 차트에 필요한 OHLV 데이터가 모두 있으면 해당 컬럼들과 Price 컬럼을 모두 반환하고,
        # 그렇지 않으면 Price 컬럼만 반환합니다.
        ohlc_cols = ['Open', 'High', 'Low', 'Close']
        if all(col in data.columns for col in ohlc_cols):
            return data[ohlc_cols + ['Price']]
        else:
            return data[['Price']]
        
    except Exception as e:
        return None

# 날짜 설정
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 3년 전

st.write(f"기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

# --- 희망 기업 선택 기능 (체크박스) ---
st.sidebar.header("기업 선택")
selected_companies_names = []
for ticker, name in TOP_10_COMPANIES.items():
    if st.sidebar.checkbox(f"{name} ({ticker})", value=True): # 기본적으로 모든 기업 체크
        selected_companies_names.append(name)

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

if selected_tickers: # 선택된 기업이 있을 때만 데이터 로드 시도
    for i, (ticker, name) in enumerate(selected_tickers.items()):
        message_placeholder.text(f"데이터 가져오는 중: {name} ({ticker})...")
        
        data_df = get_stock_data(ticker, start_date, end_date)
        
        if data_df is not None and not data_df.empty:
            all_stock_data_raw[name] = data_df
            if 'Price' in data_df.columns:
                all_price_data[name] = data_df['Price']
        progress_bar.progress((i + 1) / len(selected_tickers))

    message_placeholder.empty()
    progress_bar_placeholder.empty()

    if not all_price_data.empty:
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
        st.warning("데이터를 가져오는 데 실패했거나, 선택된 기업의 데이터가 없습니다. 티커 목록을 확인하거나 잠시 후 다시 시도해 주세요.")

else:
    message_placeholder.empty()
    progress_bar_placeholder.empty()
    st.info("표시할 기업을 선택해주세요.")

---

## 개별 기업 주가 상세 보기

chart_type = st.radio(
    "어떤 형식으로 주가를 보시겠습니까?",
    ('종가 라인 차트', '종가 영역 차트', '캔들스틱 차트 (OHLC 데이터 필요)')
)

available_for_details = list(all_stock_data_raw.keys())
    
if available_for_details:
    selected_company_for_details = st.selectbox(
        "상세 차트를 보고 싶은 기업을 선택하세요:",
        options=available_for_details
    )

    if selected_company_for_details:
        ticker_symbol_for_details = [k for k, v in TOP_10_COMPANIES.items() if v == selected_company_for_details][0]
        
        st.write(f"**{selected_company_for_details} ({ticker_symbol_for_details})**")
        
        detail_data = all_stock_data_raw.get(selected_company_for_details) # 캐시된 데이터 사용

        if detail_data is not None and not detail_data.empty:
            if chart_type == '종가 라인 차트':
                if 'Price' in detail_data.columns:
                    fig_line = go.Figure(data=[go.Scatter(x=detail_data.index, y=detail_data['Price'], mode='lines', name='종가')])
                    fig_line.update_layout(
                        title=f"{selected_company_for_details} 종가 라인 차트",
                        xaxis_title="날짜",
                        yaxis_title="주가",
                        height=500
                    )
                    st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.warning(f"{selected_company_for_details} 의 종가(Price) 데이터를 찾을 수 없어 라인 차트를 그릴 수 없습니다.")

            elif chart_type == '종가 영역 차트':
                if 'Price' in detail_data.columns:
                    fig_area = go.Figure(data=[go.Scatter(x=detail_data.index, y=detail_data['Price'], mode='lines', fill='tozeroy', name='종가')])
                    fig_area.update_layout(
                        title=f"{selected_company_for_details} 종가 영역 차트",
                        xaxis_title="날짜",
                        yaxis_title="주가",
                        height=500
                    )
                    st.plotly_chart(fig_area, use_container_width=True)
                else:
                    st.warning(f"{selected_company_for_details} 의 종가(Price) 데이터를 찾을 수 없어 영역 차트를 그릴 수 없습니다.")

            elif chart_type == '캔들스틱 차트 (OHLC 데이터 필요)':
                required_ohlc_cols = ['Open', 'High', 'Low', 'Close']
                # 캔들스틱 차트를 그리는 데 필요한 모든 컬럼이 존재하고 비어있지 않은지 다시 확인
                if all(col in detail_data.columns and not detail_data[col].empty for col in required_ohlc_cols):
                    fig_candlestick = go.Figure(data=[go.Candlestick(
                        x=detail_data.index,
                        open=detail_data['Open'],
                        high=detail_data['High'],
                        low=detail_data['Low'],
                        close=detail_data['Close']
                    )])

                    fig_candlestick.update_layout(
                        title=f"{selected_company_for_details} 캔들스틱 차트",
                        xaxis_title="날짜",
                        yaxis_title="주가",
                        xaxis_rangeslider_visible=False,
                        height=500
                    )
                    st.plotly_chart(fig_candlestick, use_container_width=True)
                else:
                    st.warning(f"{selected_company_for_details} 의 캔들스틱 차트를 그리는 데 필요한 데이터(Open, High, Low, Close)가 불완전합니다. 다른 차트 형식을 선택하세요.")

        else:
            st.warning(f"{selected_company_for_details} 의 상세 차트 데이터를 가져올 수 없습니다. 다시 시도하거나 다른 기업을 선택하세요.")

else:
    st.info("선택된 기업 중 주식 데이터를 성공적으로 가져온 기업이 없습니다. 상세 차트를 표시할 수 없습니다.")

st.markdown("---")
st.info("데이터는 Yahoo Finance에서 가져오며, 지연될 수 있습니다. 시가총액 상위 기업 목록은 시간에 따라 변경될 수 있으므로, 최신 정보를 반영하려면 `TOP_10_COMPANIES` 딕셔너리를 업데이트해야 합니다.")
