import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("이차함수 그래프 직접 입력 (계수 방식)")
st.write("아래에 이차함수의 계수 $a, b, c$를 직접 입력하여 그래프를 확인해보세요.")

# 계수 입력 필드
col1, col2, col3 = st.columns(3)

with col1:
    a_input = st.number_input("계수 a (x^2의 계수)", value=1.0, step=0.1)
with col2:
    b_input = st.number_input("계수 b (x의 계수)", value=0.0, step=0.1)
with col3:
    c_input = st.number_input("계수 c (상수항)", value=0.0, step=0.1)

# 입력된 값으로 변수 설정
a = a_input
b = b_input
c = c_input

# x 값 범위 설정
x = np.linspace(-10, 10, 400)
y = a * x**2 + b * x + c

# Plotly 그래프 생성
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {a}x^2 + {b}x + {c}'))

# 그래프 레이아웃 설정
fig.update_layout(
    title="이차함수 그래프",
    xaxis_title="x",
    yaxis_title="y",
    xaxis_range=[-10, 10],
    yaxis_range=[-20, 20],
    hovermode="x unified"
)

# x축과 y축 원점 표시
fig.add_shape(type="line", x0=-10, y0=0, x1=10, y1=0, line=dict(color="black", width=0.5))
fig.add_shape(type="line", x0=0, y0=-20, x1=0, y1=20, line=dict(color="black", width=0.5))

st.plotly_chart(fig, use_container_width=True)

st.subheader("그래프 주요 특징")
if a != 0:
    axis_of_symmetry = -b / (2 * a)
    vertex_y = a * axis_of_symmetry**2 + b * axis_of_symmetry + c

    st.markdown(f"**축의 방정식:** $x = {axis_of_symmetry:.2f}$")
    st.markdown(f"**꼭짓점의 좌표:** $({axis_of_symmetry:.2f}, {vertex_y:.2f})$")
    st.markdown(f"**y절편:** $(0, {c:.2f})$")

    # 꼭짓점 그래프에 표시
    fig.add_trace(go.Scatter(x=[axis_of_symmetry], y=[vertex_y], mode='markers',
                             marker=dict(size=10, color='red'),
                             name='꼭짓점',
                             hoverinfo='text',
                             text=f'꼭짓점: ({axis_of_symmetry:.2f}, {vertex_y:.2f})'))
    st.plotly_chart(fig, use_container_width=True) # 꼭짓점 추가된 그래프 다시 표시
else:
    st.write("`a`가 0이면 이차함수가 아니라 일차함수 또는 상수함수입니다.")
    st.write(f"현재 함수는 $y = {b}x + {c}$ 입니다.")
