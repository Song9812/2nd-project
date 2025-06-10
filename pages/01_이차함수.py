import streamlit as st
import numpy as np
import plotly.graph_objects as go # Plotly 그래프 객체 임포트

st.title("이차함수 그래프 탐구 (Plotly 버전)")
st.write("슬라이더를 움직여 이차함수 $y = ax^2 + bx + c$의 그래프 변화를 확인해보세요.")

# 사이드바에 슬라이더 배치
with st.sidebar:
    st.header("계수 설정")
    a = st.slider("a (볼록성 및 폭)", -5.0, 5.0, 1.0, 0.1)
    b = st.slider("b (축의 위치)", -10.0, 10.0, 0.0, 0.1)
    c = st.slider("c (y절편)", -10.0, 10.0, 0.0, 0.1)

# x 값 범위 설정
x = np.linspace(-10, 10, 400) # x축 범위와 해상도 설정
# 이차함수 y 값 계산
y = a * x**2 + b * x + c

# Plotly 그래프 생성
fig = go.Figure()

# 이차함수 그래프 추가
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {a}x^2 + {b}x + {c}'))

# 그래프 레이아웃 설정
fig.update_layout(
    title="이차함수 그래프",
    xaxis_title="x",
    yaxis_title="y",
    xaxis_range=[-10, 10], # x축 범위 고정
    yaxis_range=[-20, 20], # y축 범위 고정 (필요에 따라 조절)
    hovermode="x unified" # 마우스 오버 시 x축 기준으로 정보 표시
)

# x축과 y축 원점 표시
fig.add_shape(type="line", x0=-10, y0=0, x1=10, y1=0,
              line=dict(color="black", width=0.5)) # x축
fig.add_shape(type="line", x0=0, y0=-20, x1=0, y1=20,
              line=dict(color="black", width=0.5)) # y축

# Streamlit에 Plotly 그래프 표시
st.plotly_chart(fig, use_container_width=True)

# 추가 정보 (꼭짓점, 축의 방정식, y절편 등)
st.subheader("그래프 주요 특징")
if a != 0: # a가 0이 아니어야 이차함수
    axis_of_symmetry = -b / (2 * a)
    vertex_y = a * axis_of_symmetry**2 + b * axis_of_symmetry + c

    st.markdown(f"**축의 방정식:** $x = {axis_of_symmetry:.2f}$")
    st.markdown(f"**꼭짓점의 좌표:** $({axis_of_symmetry:.2f}, {vertex_y:.2f})$")
    st.markdown(f"**y절편:** $(0, {c:.2f})$")

    # 꼭짓점 그래프에 표시 (선택 사항)
    fig.add_trace(go.Scatter(x=[axis_of_symmetry], y=[vertex_y], mode='markers',
                             marker=dict(size=10, color='red'),
                             name='꼭짓점',
                             hoverinfo='text',
                             text=f'꼭짓점: ({axis_of_symmetry:.2f}, {vertex_y:.2f})'))

    st.plotly_chart(fig, use_container_width=True) # 꼭짓점 추가된 그래프 다시 표시
else:
    st.write("`a`가 0이면 이차함수가 아니라 일차함수 또는 상수함수입니다.")
    st.write(f"현재 함수는 $y = {b}x + {c}$ 입니다.")
