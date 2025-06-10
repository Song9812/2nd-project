import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide") # 페이지 넓이 설정 (선택 사항)

st.title("이차함수 계수 부호 맞추기 퀴즈 📈")
st.write("제시된 이차함수 그래프를 보고, 계수 $a, b, c$의 부호를 맞춰보세요!")

# 세션 상태 초기화 (앱이 처음 로드되거나 새로고침될 때만 실행)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = {}
    st.session_state.quiz_data['a'] = 0
    st.session_state.quiz_data['b'] = 0
    st.session_data['c'] = 0
    st.session_state.quiz_data['question_number'] = 0
    st.session_state.quiz_data['correct_count'] = 0
    st.session_state.quiz_data['show_answer'] = False
    generate_new_question() # 첫 문제 생성

# --- 함수 정의 ---
def generate_random_coefficients():
    """랜덤으로 이차함수 계수 a, b, c를 생성합니다."""
    # a: 0이 아니어야 이차함수. 폭과 볼록성 결정.
    a = random.choice([-3, -2, -1, 1, 2, 3]) # 0 제외
    
    # b: 축의 위치 결정. b가 0일 때도 있게 함.
    b = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    
    # c: y절편 결정. c가 0일 때도 있게 함.
    c = random.choice([-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7])
    
    return a, b, c

def get_sign(value):
    """숫자의 부호를 반환합니다 ('양수', '음수', '0')."""
    if value > 0:
        return "양수"
    elif value < 0:
        return "음수"
    else:
        return "0"

def generate_new_question():
    """새로운 퀴즈 문제를 생성하고 세션 상태에 저장합니다."""
    a, b, c = generate_random_coefficients()
    
    # 정답 부호 추출
    correct_a_sign = get_sign(a)
    correct_b_sign = get_sign(b)
    
    # 축의 방정식 -b/2a를 이용한 b의 부호 결정
    # 그래프를 보고 b의 부호를 유추하는 것은 a의 부호와 함께 축의 위치를 봐야 하므로 좀 더 복잡합니다.
    # 여기서는 단순하게 b 자체의 부호를 정답으로 합니다.
    # 고급 버전에서는 축의 방정식과 a의 부호를 조합하여 '축의 위치'를 묻는 방식으로 변경 가능
    
    correct_c_sign = get_sign(c)

    st.session_state.quiz_data['a'] = a
    st.session_state.quiz_data['b'] = b
    st.session_state.quiz_data['c'] = c
    st.session_state.quiz_data['correct_a_sign'] = correct_a_sign
    st.session_state.quiz_data['correct_b_sign'] = correct_b_sign
    st.session_state.quiz_data['correct_c_sign'] = correct_c_sign
    st.session_state.quiz_data['show_answer'] = False # 정답 숨기기
    st.session_state.quiz_data['question_number'] += 1 # 문제 번호 증가

# --- 그래프 그리기 함수 ---
def plot_quadratic_function(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {a}x^2 + {b}x + {c}'))

    fig.update_layout(
        title="이차함수 그래프",
        xaxis_title="x",
        yaxis_title="y",
        xaxis_range=[-10, 10],
        yaxis_range=[-20, 20], # y축 범위는 필요에 따라 조정
        hovermode="x unified",
        height=400 # 그래프 높이 고정
    )

    fig.add_shape(type="line", x0=-10, y0=0, x1=10, y1=0, line=dict(color="black", width=0.5)) # x축
    fig.add_shape(type="line", x0=0, y0=-20, x1=0, y1=20, line=dict(color="black", width=0.5)) # y축
    
    # 꼭짓점 표시 (선택 사항)
    if a != 0:
        axis_of_symmetry = -b / (2 * a)
        vertex_y = a * axis_of_symmetry**2 + b * axis_of_symmetry + c
        fig.add_trace(go.Scatter(x=[axis_of_symmetry], y=[vertex_y], mode='markers',
                                 marker=dict(size=8, color='red'),
                                 name='꼭짓점',
                                 hoverinfo='text',
                                 text=f'꼭짓점: ({axis_of_symmetry:.2f}, {vertex_y:.2f})'))

    st.plotly_chart(fig, use_container_width=True)

# --- 퀴즈 UI ---
st.header(f"문제 #{st.session_state.quiz_data['question_number']}")

# 현재 문제의 계수로 그래프 그리기
plot_quadratic_function(
    st.session_state.quiz_data['a'],
    st.session_state.quiz_data['b'],
    st.session_state.quiz_data['c']
)

st.subheader("각 계수의 부호는 무엇일까요?")

# 사용자 입력 받기
col_a, col_b, col_c = st.columns(3)
with col_a:
    user_a_sign = st.selectbox("계수 a", ["선택", "양수", "음수"])
with col_b:
    user_b_sign = st.selectbox("계수 b", ["선택", "양수", "음수", "0"]) # b가 0일 수도 있음
with col_c:
    user_c_sign = st.selectbox("계수 c", ["선택", "양수", "음수", "0"]) # c가 0일 수도 있음

submit_button = st.button("정답 확인 ✅")
new_question_button = st.button("새로운 문제 🔄")

if submit_button:
    st.session_state.quiz_data['show_answer'] = True # 정답을 보여주도록 설정

    # 정답 확인 로직
    is_a_correct = (user_a_sign == st.session_state.quiz_data['correct_a_sign'])
    is_b_correct = (user_b_sign == st.session_state.quiz_data['correct_b_sign'])
    is_c_correct = (user_c_sign == st.session_state.quiz_data['correct_c_sign'])

    st.subheader("결과:")
    if is_a_correct and is_b_correct and is_c_correct:
        st.success("🎉 정답입니다! 모든 부호를 맞췄어요!")
        st.session_state.quiz_data['correct_count'] += 1
    else:
        st.error("😢 아쉽지만 틀렸습니다. 다시 시도해보세요.")
        st.write(f"현재까지 맞춘 문제: {st.session_state.quiz_data['correct_count']}개 / {st.session_state.quiz_data['question_number'] -1}개") # 현재 문제를 제외하고 카운트

    # 정답 표시 (선택 사항)
    if st.session_state.quiz_data['show_answer']:
        st.info(f"**정답:**\n"
                f"- 계수 a: **{st.session_state.quiz_data['correct_a_sign']}** ({'O' if is_a_correct else 'X'}) \n"
                f"- 계수 b: **{st.session_state.quiz_data['correct_b_sign']}** ({'O' if is_b_correct else 'X'})\n"
                f"- 계수 c: **{st.session_state.quiz_data['correct_c_sign']}** ({'O' if is_c_correct else 'X'})")

elif new_question_button:
    generate_new_question() # 새로운 문제 생성
    st.rerun() # 앱을 다시 실행하여 새 문제와 UI를 즉시 반영

# 전체 맞춘 문제 수 및 현재 진행 상태 표시
st.sidebar.markdown("---")
st.sidebar.subheader("퀴즈 진행 상황")
st.sidebar.write(f"현재 문제 번호: {st.session_state.quiz_data['question_number']}")
st.sidebar.write(f"맞춘 문제 수: {st.session_state.quiz_data['correct_count']}")
