import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시총 Top 10 기업 주가 변화 (최근 3년)")

# 글로벌 시총 Top 10 기업 (2025년 6월 기준 예상, 변동될 수 있음)
# 실제 시총 순위는 계속 변동하므로, 필요한 경우 업데이트해주세요.
# 여기서는 대표적인 기술 기업들을 중심으로 선정했습니다.
# 이 목록은 시간이 지남에 따라 변할 수 있습니다.
TOP_10_COMPANIES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet (Google) A",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "META": "Meta Platforms",
    "TSLA": "Tesla",
    "BRK-A": "Berkshire Hathaway A", # B 클래스도 고려 가능 BRK-B
    "JPM": "JPMorgan Chase", # 금융주 대표
    "LLY": "Eli Lilly and Company", # 헬스케어 대표
    # 다른 후보: V (Visa), JNJ (Johnson & Johnson), XOM (Exxon Mobil), TSM (TSMC), UNH (UnitedHealth Group)
}

@st.cache_data
def get_stock_data(ticker_symbol, start_date, end_date):
    """지정된 티커의 주식 데이터를 가져옵니다."""
    try:
        data = yf.download(ticker_symbol, start=start_date, end=end_date)
        if data.empty:
            st.warning(f"{ticker_symbol} 에 대한 데이터가 없습니다.")
            return None
        return data['Adj Close'] # 수정 종가 사용
    except Exception as e:
        st.error(f"{ticker_symbol} 데이터를 가져오는 중 오류 발생: {e}")
        return None

# 날짜 설정
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 3년 전

st.write(f"기간: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

# 모든 기업의 데이터 가져오기
all_stock_data = pd.DataFrame()
progress_bar = st.progress(0)
for i, (ticker, name) in enumerate(TOP_10_COMPANIES.items()):
    st.text(f"데이터 가져오는 중: {name} ({ticker})...")
    data = get_stock_data(ticker, start_date, end_date)
    if data is not None:
        all_stock_data[name] = data
    progress_bar.progress((i + 1) / len(TOP_10_COMPANIES))

if not all_stock_data.empty:
    # 초기 가격을 100으로 정규화하여 변화율 비교
    normalized_data = all_stock_data / all_stock_data.iloc[0] * 100

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

    st.markdown("---")
    st.subheader("개별 기업 주가 상세 보기")

    selected_company = st.selectbox(
        "기업을 선택하세요:",
        options=list(TOP_10_COMPANIES.values())
    )

    if selected_company:
        ticker_symbol = [k for k, v in TOP_10_COMPANIES.items() if v == selected_company][0]
        
        st.write(f"**{selected_company} ({ticker_symbol})**")
        
        # 캔들스틱 차트 그리기
        candlestick_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        
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
    st.error("데이터를 가져오는 데 실패했습니다. 티커 목록을 확인하거나 잠시 후 다시 시도해 주세요.")

st.markdown("---")
st.info("데이터는 Yahoo Finance에서 가져오며, 지연될 수 있습니다. 시가총액 상위 기업 목록은 시간에 따라 변경될 수 있으므로, 최신 정보를 반영하려면 `TOP_10_COMPANIES` 딕셔너리를 업데이트해야 합니다.")
