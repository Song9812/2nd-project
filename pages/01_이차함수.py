import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

# 페이지 레이아웃 설정 (선택 사항: 페이지를 더 넓게 사용)
st.set_page_config(layout="wide")

st.title("이차함수 계수 부호 맞추기 퀴즈 📈")
st.write("제시된 이차함수 그래프를 보고, 계수 $a, b, c$의 부호를 맞춰보세요!")

# --- 세션 상태 초기화 및 문제 생성 함수 ---

def generate_random_coefficients():
    """랜덤으로 이차함수 계수 a, b, c를 생성합니다."""
    # a: 0이 아니어야 이차함수. 볼록성과 폭을 결정합니다.
    # 학생들이 볼록성을 직관적으로 파악할 수 있도록 비교적 큰 값은 피합니다.
    a = random.choice([-3, -2, -1, 1, 2, 3]) # 0 제외

    # b: 축의 위치를 결정합니다. 0일 수도 있습니다.
    b = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

    # c: y절편을 결정합니다. 0일 수도 있습니다.
    c = random.choice([-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7])

    return a, b, c

def get_sign(value):
    """숫자의 부호를 문자열로 반환합니다 ('양수', '음수', '0')."""
    if value > 0:
        return "양수"
    elif value < 0:
        return "음수"
    else:
        return "0"

def setup_new_question_data():
    """새로운 문제에 대한 데이터를 생성하여 세션 상태에 저장하고, 문제 번호를 증가시킵니다."""
    a, b, c = generate_random_coefficients()
    st.session_state.quiz_data['a'] = a
    st.session_state.quiz_data['b'] = b
    st.session_state.quiz_data['c'] = c
    st.session_state.quiz_data['correct_a_sign'] = get_sign(a)
    st.session_state.quiz_data['correct_b_sign'] = get_sign(b)
    st.session_state.quiz_data['correct_c_sign'] = get_sign(c)
    st.session_state.quiz_data['show_answer'] = False # 정답 숨기기
    st.session_state.quiz_data['question_number'] += 1 # 문제 번호 증가

# --- 세션 상태 초기화: 모든 필요한 키가 존재하는지 확인하고, 없으면 기본값 할당 ---
# 이 블록은 앱이 실행될 때마다 검사되어, 세션 상태가 항상 올바르게 초기화되도록 보장합니다.

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = {}

# quiz_data 내의 모든 필요한 키들을 개별적으로 확인하고 초기화합니다.
# 이렇게 하면 특정 키가 누락되었을 때도 안전하게 기본값을 설정할 수 있습니다.
if 'a' not in st.session_state.quiz_data:
    st.session_state.quiz_data['a'] = 0
if 'b' not in st.session_state.quiz_data:
    st.session_state.quiz_data['b'] = 0
if 'c' not in st.session_state.quiz_data:
    st.session_state.quiz_data['c'] = 0
if 'correct_a_sign' not in st.session_state.quiz_data:
    st.session_state.quiz_data['correct_a_sign'] = ''
if 'correct_b_sign' not in st.session_state.quiz_data:
    st.session_state.quiz_data['correct_b_sign'] = ''
if 'correct_c_sign' not in st.session_state.quiz_data:
    st.session_state.quiz_data['correct_c_sign'] = ''
if 'question_number' not in st.session_state.quiz_data:
    st.session_state.quiz_data['question_number'] = 0 # 초기값 0
if 'correct_count' not in st.session_state.quiz_data:
    st.session_state.quiz_data['correct_count'] = 0
if 'show_answer' not in st.session_state.quiz_data:
    st.session_state.quiz_data['show_answer'] = False

# 앱이 처음 시작될 때만 첫 문제를 설정합니다.
# question_number가 0인 상태는 앱이 처음 로드되었을 때만 해당합니다.
if st.session_state.quiz_data['question_number'] == 0:
    setup_new_question_data()


# --- 그래프 그리기 함수 ---
def plot_quadratic_function(a, b, c):
    """주어진 계수로 이차함수 그래프를 Plotly로 그립니다."""
    x = np.linspace(-10, 10, 400) # x축 범위와 해상도 설정
    y = a * x**2 + b * x + c     # 이차함수 y 값 계산

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines',
                             name=f'y = {a}x² + {b}x + {c}')) # Plotly는 텍스트에 ² 직접 사용 가능

    # 그래프 레이아웃 설정
    fig.update_layout(
        title="이차함수 그래프",
        xaxis_title="x",
        yaxis_title="y",
        xaxis_range=[-10, 10],   # x축 범위 고정
        yaxis_range=[-20, 20],   # y축 범위 고정 (그래프가 너무 커지지 않게 조정)
        hovermode="x unified",   # 마우스 오버 시 x축 기준으로 정보 표시
        height=400,              # 그래프 높이 고정
        showlegend=False         # 범례 숨김 (함수식이 제목에 표시되므로)
    )

    # x축과 y축 원점 표시 (Plotly shapes 사용)
    fig.add_shape(type="line", x0=-10, y0=0, x1=10, y1=0,
                  line=dict(color="black", width=0.5)) # x축
    fig.add_shape(type="line", x0=0, y0=-20, x1=0, y1=20,
                  line=dict(color="black", width=0.5)) # y축

    # 꼭짓점 표시 (선택 사항: 학생들에게 힌트가 될 수 있음)
    if a != 0:
        axis_of_symmetry = -b / (2 * a)
        vertex_y = a * axis_of_symmetry**2 + b * axis_of_symmetry + c
        fig.add_trace(go.Scatter(x=[axis_of_symmetry], y=[vertex_y], mode='markers',
                                 marker=dict(size=8, color='red'),
                                 name='꼭짓점',
                                 hoverinfo='text',
                                 text=f'꼭짓점: ({axis_of_symmetry:.2f}, {vertex_y:.2f})'))

    st.plotly_chart(fig, use_container_width=True) # Streamlit에 Plotly 그래프 표시

# --- 퀴즈 UI ---

# 이 부분은 'question_number'가 항상 존재한다고 가정하므로, 위에서 초기화가 중요합니다.
st.header(f"문제 #{st.session_state.quiz_data['question_number']}")

# 현재 문제의 계수로 그래프 그리기
plot_quadratic_function(
    st.session_state.quiz_data['a'],
    st.session_state.quiz_data['b'],
    st.session_state.quiz_data['c']
)

st.subheader("각 계수의 부호는 무엇일까요?")

# 사용자 입력 드롭다운 메뉴
col_a, col_b, col_c = st.columns(3)
with col_a:
    user_a_sign = st.selectbox("계수 a (볼록성)", ["선택", "양수", "음수"], key="a_select")
with col_b:
    user_b_sign = st.selectbox("계수 b (축의 위치)", ["선택", "양수", "음수", "0"], key="b_select")
with col_c:
    user_c_sign = st.selectbox("계수 c (y절편)", ["선택", "양수", "음수", "0"], key="c_select")

# 버튼 배치
col_buttons1, col_buttons2 = st.columns([1, 1])
with col_buttons1:
    submit_button = st.button("정답 확인 ✅", use_container_width=True)
with col_buttons2:
    new_question_button = st.button("새로운 문제 🔄", use_container_width=True)

# --- 버튼 클릭 이벤트 처리 ---
if submit_button:
    # 정답 확인 후 정답 표시 플래그를 True로 설정
    st.session_state.quiz_data['show_answer'] = True

    # 사용자 입력과 실제 정답 비교
    is_a_correct = (user_a_sign == st.session_state.quiz_data['correct_a_sign'])
    is_b_correct = (user_b_sign == st.session_state.quiz_data['correct_b_sign'])
    is_c_correct = (user_c_sign == st.session_state.quiz_data['correct_c_sign'])

    st.subheader("결과:")
    if is_a_correct and is_b_correct and is_c_correct:
        st.success("🎉 정답입니다! 모든 부호를 맞췄어요!")
        st.session_state.quiz_data['correct_count'] += 1
    else:
        st.error("😢 아쉽지만 틀렸습니다. 다시 시도해보세요.")
        st.write(f"현재까지 맞춘 문제: **{st.session_state.quiz_data['correct_count']}개** / **{st.session_state.quiz_data['question_number'] -1}개**") # 현재 문제는 제외하고 카운트

    # 정답 정보 표시
    if st.session_state.quiz_data['show_answer']:
        st.info(f"**정답:**\n"
                f"- 계수 a: **{st.session_state.quiz_data['correct_a_sign']}** ({'O' if is_a_correct else 'X'}) \n"
                f"- 계수 b: **{st.session_state.quiz_data['correct_b_sign']}** ({'O' if is_b_correct else 'X'})\n"
                f"- 계수 c: **{st.session_state.quiz_data['correct_c_sign']}** ({'O' if is_c_correct else 'X'})")

elif new_question_button:
    # 새로운 문제 생성 후 앱 다시 실행 (UI 업데이트)
    setup_new_question_data() # 새로운 문제 데이터 설정
    st.rerun() # 앱의 전체 스크립트를 다시 실행하여 변경 사항을 즉시 반영

# --- 퀴즈 진행 상황 대시보드 (사이드바) ---
st.sidebar.markdown("---")
st.sidebar.subheader("퀴즈 진행 상황")
st.sidebar.write(f"총 문제 수: **{st.session_state.quiz_data['question_number']}**")
st.sidebar.write(f"맞춘 문제 수: **{st.session_state.quiz_data['correct_count']}**")
