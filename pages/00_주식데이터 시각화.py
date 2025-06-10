import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit 페이지 설정
st.set_page_config(layout="wide")

st.title("글로벌 시총 Top 10 기업 주가 변화")

# 글로벌 시총 Top 10 기업 목록 (티커: 이름)
# 이 목록은 시간이 지남에 따라 변경될 수 있으므로, 필요 시 업데이트하세요.
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

@st.cache_data # 데이터 캐싱 (성능 향상)
def get_stock_data(ticker_symbol, start_date, end_date):
    """
    지정된 티커의 주식 데이터를 가져옵니다.
    'Adj Close'가 없으면 'Close'를 사용하고, 캔들스틱 차트용 OHLC 데이터도 포함합니다.
    """
    try:
        # yfinance로 주식 데이터 다운로드 (진행 메시지 비활성화)
        data = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)

        # 데이터가 비어있으면 None 반환
        if data.empty:
            return None
        
        # 'Adj Close' 컬럼이 있으면 우선 사용, 없으면 'Close' 컬럼 사용
        if 'Adj Close' in data.columns and not data['Adj Close'].empty:
            data['Price'] = data['Adj Close']
        elif 'Close' in data.columns and not data['Close'].empty:
            data['Price'] = data['Close']
        else:
            # 주가 데이터(Price)를 만들 수 없으면 None 반환
            return None

        # 캔들스틱 차트에 필요한 OHLC (Open, High, Low, Close) 컬럼이 모두 있는지 확인
        ohlc_cols = ['Open', 'High', 'Low', 'Close']
        if all(col in data.columns and not data[col].empty for col in ohlc_cols):
            # OHLC와 Price 컬럼을 모두 포함하는 DataFrame 반환
            return data[ohlc_cols + ['Price']]
        else:
            # OHLC 데이터가 불완전하면 Price 컬럼만 포함하는 DataFrame 반환
            return data[['Price']]
        
    except Exception as e:
        # 데이터 가져오기 중 예외 발생 시 None 반환
        # st.error(f"티커 '{ticker_symbol}'의 데이터를 가져오는 중 오류 발생: {e}") # 개발 시 주석 해제하여 디버깅
        return None

# 최근 3년 데이터 기간 설정
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 대략 3년 전

st.write(f"데이터 기간: **{start_date.strftime('%Y-%m-%d')}** ~ **{end_date.strftime('%Y-%m-%d')}**")

# --- 사이드바: 기업 선택 체크박스 기능 ---
st.sidebar.header("보고 싶은 기업 선택")
selected_companies_names = []
# 모든 TOP_10_COMPANIES에 대해 체크박스 생성 (기본값 True로 모두 선택)
for ticker, name in TOP_10_COMPANIES.items():
    if st.sidebar.checkbox(f"{name} ({ticker})", value=True, key=ticker):
        selected_companies_names.append(name)

# 선택된 기업의 티커-이름 매핑 딕셔너리 생성
selected_tickers = {ticker: name for ticker, name in TOP_10_COMPANIES.items() if name in selected_companies_names}
# --- 사이드바 끝 ---

# 데이터 로딩 상태 표시
st.subheader("주식 데이터 가져오기 진행 중...")
progress_bar_placeholder = st.empty() # 진행 바를 위한 플레이스홀더
progress_bar = progress_bar_placeholder.progress(0) # 진행 바 초기화
message_placeholder = st.empty() # 메시지를 위한 플레이스홀더

# 모든 기업의 데이터를 저장할 딕셔너리와 DataFrame 초기화
all_stock_data_raw = {} # 개별 기업의 상세 데이터 (OHLC, Price)
all_price_data = pd.DataFrame() # 라인 그래프용 정규화 가격 데이터

# 선택된 기업이 있을 경우에만 데이터 로드 시도
if selected_tickers:
    for i, (ticker, name) in enumerate(selected_tickers.items()):
        message_placeholder.text(f"데이터 가져오는 중: {name} ({ticker})...")
        
        data_df = get_stock_data(ticker, start_date, end_date)
        
        if data_df is not None and not data_df.empty:
            all_stock_data_raw[name] = data_df
            # Price 컬럼이 있는지 확인하고 all_price_data에 추가
            if 'Price' in data_df.columns:
                all_price_data[name] = data_df['Price']
        
        # 진행 바 업데이트
        progress_bar.progress((i + 1) / len(selected_tickers))

    # 모든 데이터 로드 후 플레이스홀더 비우기
    message_placeholder.empty()
    progress_bar_placeholder.empty()

    # --- 메인 그래프: 정규화된 주가 변화 ---
    if not all_price_data.empty:
        # 모든 값이 NaN인 컬럼(데이터 로드 실패 기업) 제거 후 정규화
        normalized_data = all_price_data.dropna(axis=1, how='all')
        if not normalized_data.empty:
            # 초기 가격을 100으로 정규화하여 변화율 비교
            # 첫 번째 행으로 나누어 정규화. (loc[0] 대신 iloc[0] 사용)
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
        st.warning("데이터를 가져오는 데 실패했거나, 선택된 기업의 유효한 주가 데이터가 없습니다. 티커 목록을 확인하거나 잠시 후 다시 시도해 주세요.")

else:
    # 선택된 기업이 없을 경우 메시지 표시
    message_placeholder.empty()
    progress_bar_placeholder.empty()
    st.info("표시할 기업을 선택해주세요. 왼쪽 사이드바에서 기업을 선택할 수 있습니다.")

st.markdown("---") # 시각적 구분선

## 개별 기업 주가 상세 보기 (차트 형식 선택)
st.subheader("개별 기업 주가 상세 보기")

# 차트 형식 선택 라디오 버튼
chart_type = st.radio(
    "어떤 형식으로 주가를 보시겠습니까?",
    ('종가 라인 차트', '종가 영역 차트', '캔들스틱 차트 (OHLC 데이터 필요)'),
    index=0 # 기본값으로 '종가 라인 차트' 선택
)

# 데이터가 성공적으로 로드된 기업만 상세 보기 옵션에 포함
available_for_details = list(all_stock_data_raw.keys())
    
if available_for_details:
    selected_company_for_details = st.selectbox(
        "상세 차트를 보고 싶은 기업을 선택하세요:",
        options=available_for_details
    )

    if selected_company_for_details:
        # 선택된 기업의 티커 심볼 찾기
        ticker_symbol_for_details = [k for k, v in TOP_10_COMPANIES.items() if v == selected_company_for_details][0]
        
        st.write(f"**{selected_company_for_details} ({ticker_symbol_for_details})**")
        
        # 캐시된 데이터(all_stock_data_raw)에서 상세 데이터 가져오기
        detail_data = all_stock_data_raw.get(selected_company_for_details)

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
                        xaxis_rangeslider_visible=False, # 범위 슬라이더 제거
                        height=500
                    )
                    st.plotly_chart(fig_candlestick, use_container_width=True)
                else:
                    st.warning(f"{selected_company_for_details} 의 캔들스틱 차트를 그리는 데 필요한 데이터(Open, High, Low, Close)가 불완전합니다. 다른 차트 형식을 선택하거나, 이 기업의 OHLC 데이터가 Yahoo Finance에 없을 수 있습니다.")

        else:
            st.warning(f"{selected_company_for_details} 의 상세 차트 데이터를 가져올 수 없습니다. 다시 시도하거나 다른 기업을 선택하세요.")

else:
    st.info("선택된 기업 중 주식 데이터를 성공적으로 가져온 기업이 없습니다. 상세 차트를 표시할 수 없습니다.")

st.markdown("---") # 시각적 구분선
st.info("데이터는 Yahoo Finance에서 가져오며, 지연될 수 있습니다. 시가총액 상위 기업 목록은 시간에 따라 변경될 수 있으므로, 최신 정보를 반영하려면 `TOP_10_COMPANIES` 딕셔너리를 업데이트해야 합니다.")
