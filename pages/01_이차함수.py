import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("이차함수 그래프 탐구")

# 슬라이더로 a, b, c 값 설정
a = st.slider("a", -5.0, 5.0, 1.0, 0.1)
b = st.slider("b", -10.0, 10.0, 0.0, 0.1)
c = st.slider("c", -10.0, 10.0, 0.0, 0.1)

# x 값 범위 설정
x = np.linspace(-10, 10, 400)
# 이차함수 y 값 계산
y = a * x**2 + b * x + c

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(x, y, label=f"y = {a}x^2 + {b}x + {c}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("이차함수 그래프")
ax.grid(True)
ax.axhline(0, color='black', linewidth=0.5) # x축
ax.axvline(0, color='black', linewidth=0.5) # y축
ax.legend()
ax.set_ylim(-20, 20) # y축 범위 고정 (선택 사항)

st.pyplot(fig)

# 추가 정보 (꼭짓점, 축의 방정식 등)
if a != 0: # a가 0이 아니어야 이차함수
    axis_of_symmetry = -b / (2 * a)
    vertex_y = a * axis_of_symmetry**2 + b * axis_of_symmetry + c
    st.write(f"**축의 방정식:** $x = {axis_of_symmetry:.2f}$")
    st.write(f"**꼭짓점의 좌표:** $({axis_of_symmetry:.2f}, {vertex_y:.2f})$")
    st.write(f"**y절편:** $(0, {c:.2f})$")
else:
    st.write("a가 0이면 이차함수가 아닙니다.")
