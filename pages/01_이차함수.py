import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

# 페이지 레이아웃 설정
st.set_page_config(layout="wide", page_title="이차함수 탐구 앱")

# --- 세션 상태 초기화 및 공통 함수 ---

# 세션 상태 'quiz_data' 초기화. 앱이 처음 로드될 때만 실행됩니다.
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
if st.session_state.quiz_data['question_number'] == 0:
    a_initial, b_initial, c_initial = random_coefficients_for_quiz()
    st.session_state.quiz_data['a'] = a_initial
    st.session_state.quiz_data['b'] = b_initial
    st.session_state.quiz_data['c'] = c_initial
    st.session_state.quiz_data['correct_a_sign'] = get_sign(a_initial)
    st.session_state.quiz_data['correct_b_sign'] = get_sign(b_initial)
    st.session_state.quiz_data['correct_c_sign'] = get_sign(c_initial)
    st.session_state.quiz_data['question_number'] = 1 # 첫 문제 시작 시 1로 설정


def random_coefficients_for_quiz():
    """퀴즈를 위한 랜덤 이차함수 계수 a, b, c를 생성합니다."""
    a = random.choice([-3, -2, -1, 1, 2, 3]) # 0 제외
    b = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
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

def plot_quadratic_function(a, b, c, title="이차함수 그래프", y_range=[-20, 20], show_vertex=True):
    """주어진 계수로 이차함수 그래프를 Plotly로 그립니다."""
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {a}x² + {b}x + {c}'))

    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        xaxis_range=[-10, 10],
        yaxis_range=y_range,
        hovermode="x unified",
        height=400,
        showlegend=False
    )

    fig.add_shape(type="line", x0=-10, y0=0, x1=10, y1=0, line=dict(color="black", width=0.5)) # x축
    fig.add_shape(type="line", x0=0, y0=y_range[0], x1=0, y1=y_range[1], line=dict(color="black", width=0.5)) # y축

    if show_vertex and a != 0:
        axis_of_symmetry = -b / (2 * a)
        vertex_y = a * axis_of_symmetry**2 + b * axis_of_symmetry + c
        fig.add_trace(go.Scatter(x=[axis_of_symmetry], y=[vertex_y], mode='markers',
                                 marker=dict(size=8, color='red'),
                                 name='꼭짓점',
                                 hoverinfo='text',
                                 text=f'꼭짓점: ({axis_of_symmetry:.2f}, {vertex_y:.2f})'))

    st.plotly_chart(fig, use_container_width=True)


# --- 사이드바 메뉴 ---
st.sidebar.title("메뉴")
page_selection = st.sidebar.radio("페이지 선택", ["이차함수 퀴즈", "포물선 닮음 탐구"])

# --- 페이지 로직 ---
if page_selection == "이차함수 퀴즈":
    st.header(f"문제 #{st.session_state.quiz_data['question_number']}")
    
    # 현재 문제의 계수로 그래프 그리기
    plot_quadratic_function(
        st.session_state.quiz_data['a'],
        st.session_state.quiz_data['b'],
        st.session_state.quiz_data['c'],
        title="이차함수 그래프 (퀴즈)"
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
        st.session_state.quiz_data['show_answer'] = True

        is_a_correct = (user_a_sign == st.session_state.quiz_data['correct_a_sign'])
        is_b_correct = (user_b_sign == st.session_state.quiz_data['correct_b_sign'])
        is_c_correct = (user_c_sign == st.session_state.quiz_data['correct_c_sign'])

        st.subheader("결과:")
        if is_a_correct and is_b_correct and is_c_correct:
            st.success("🎉 정답입니다! 모든 부호를 맞췄어요!")
            st.session_state.quiz_data['correct_count'] += 1
        else:
            st.error("😢 아쉽지만 틀렸습니다. 다시 시도해보세요.")
            st.write(f"현재까지 맞춘 문제: **{st.session_state.quiz_data['correct_count']}개** / **{st.session_state.quiz_data['question_number'] -1}개**")

        if st.session_state.quiz_data['show_answer']:
            st.info(f"**정답:**\n"
                    f"- 계수 a: **{st.session_state.quiz_data['correct_a_sign']}** ({'O' if is_a_correct else 'X'}) \n"
                    f"- 계수 b: **{st.session_state.quiz_data['correct_b_sign']}** ({'O' if is_b_correct else 'X'})\n"
                    f"- 계수 c: **{st.session_state.quiz_data['correct_c_sign']}** ({'O' if is_c_correct else 'X'})")

    elif new_question_button:
        # 새로운 문제 생성
        a_new, b_new, c_new = random_coefficients_for_quiz()
        st.session_state.quiz_data['a'] = a_new
        st.session_state.quiz_data['b'] = b_new
        st.session_state.quiz_data['c'] = c_new
        st.session_state.quiz_data['correct_a_sign'] = get_sign(a_new)
        st.session_state.quiz_data['correct_b_sign'] = get_sign(b_new)
        st.session_state.quiz_data['correct_c_sign'] = get_sign(c_new)
        st.session_state.quiz_data['show_answer'] = False
        st.session_state.quiz_data['question_number'] += 1 # 문제 번호 증가
        st.rerun() # 앱 다시 실행

    st.sidebar.markdown("---")
    st.sidebar.subheader("퀴즈 진행 상황")
    st.sidebar.write(f"총 문제 수: **{st.session_state.quiz_data['question_number']}**")
    st.sidebar.write(f"맞춘 문제 수: **{st.session_state.quiz_data['correct_count']}**")

elif page_selection == "포물선 닮음 탐구":
    st.header("포물선 닮음 시각화 도구")
    st.write("두 포물선의 계수를 조절하고, 확대/축소 및 이동하여 포물선이 모두 닮음임을 확인해보세요.")

    # --- 포물선 1 설정 ---
    st.subheader("포물선 1 설정")
    col1_1, col1_2, col1_3 = st.columns(3)
    with col1_1:
        a1_sim = st.slider("a1 (x² 계수)", -5.0, 5.0, 1.0, step=0.1, key="sim_a1")
    with col1_2:
        b1_sim = st.slider("b1 (x 계수)", -10.0, 10.0, 0.0, step=0.1, key="sim_b1")
    with col1_3:
        c1_sim = st.slider("c1 (상수항)", -10.0, 10.0, 0.0, step=0.1, key="sim_c1")

    # --- 포물선 2 설정 ---
    st.subheader("포물선 2 설정")
    col2_1, col2_2, col2_3 = st.columns(3)
    with col2_1:
        a2_sim = st.slider("a2 (x² 계수)", -5.0, 5.0, 0.5, step=0.1, key="sim_a2")
    with col2_2:
        b2_sim = st.slider("b2 (x 계수)", -10.0, 10.0, 0.0, step=0.1, key="sim_b2")
    with col2_3:
        c2_sim = st.slider("c2 (상수항)", -10.0, 10.0, 2.0, step=0.1, key="sim_c2")

    # --- 그래프 범위 및 이동 설정 ---
    st.subheader("그래프 보기 설정")
    zoom = st.slider("확대/축소", 0.1, 5.0, 1.0, step=0.1, key="sim_zoom")
    x_offset = st.slider("x축 이동", -10.0, 10.0, 0.0, step=0.1, key="sim_x_offset")
    y_offset = st.slider("y축 이동", -20.0, 20.0, 0.0, step=0.1, key="sim_y_offset")

    # --- 그래프 생성 ---
    x_range_base = 10 / zoom
    y_range_base = 20 / zoom

    x_vals = np.linspace(-x_range_base + x_offset, x_range_base + x_offset, 400)
    y1_vals = a1_sim * x_vals**2 + b1_sim * x_vals + c1_sim
    y2_vals = a2_sim * x_vals**2 + b2_sim * x_vals + c2_sim

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y1_vals, mode='lines', name=f'포물선 1: y = {a1_sim}x² + {b1_sim}x + {c1_sim}'))
    fig.add_trace(go.Scatter(x=x_vals, y=y2_vals, mode='lines', name=f'포물선 2: y = {a2_sim}x² + {b2_sim}x + {c2_sim}'))

    # 그래프 레이아웃 설정 (확대/축소 및 이동 적용)
    fig.update_layout(
        title="두 포물선 비교",
        xaxis_title="x",
        yaxis_title="y",
        xaxis_range=[-10, 10], # 고정된 전체 보기 범위
        yaxis_range=[-20, 20], # 고정된 전체 보기 범위
        hovermode="x unified",
        height=600,
        showlegend=True
    )
    # 실제 보이는 뷰포트 범위는 x_offset, y_offset, zoom에 따라 조정됩니다.
    # plotly_chart에 직접 zoom과 offset을 적용하기보다는, x_vals, y_vals를 해당 범위로 생성하는 방식이 더 자연스럽습니다.
    # 하지만 사용자의 시각적 조정 편의성을 위해 range를 슬라이더로 직접 조절하는 방식은 좀 더 직관적일 수 있습니다.

    # 여기서는 고정된 전체 범위를 보여주고, 사용자가 스크롤/줌으로 탐색하도록 Plotly 기본 기능을 활용합니다.
    # 만약 슬라이더로 엄격하게 범위 제어를 원한다면, x_vals 생성 로직을 변경해야 합니다.
    # 현재 코드는 사용자가 슬라이더를 움직여도 그래프가 전체 범위에서 그려진 후, Plotly 내부의 줌/패닝 기능처럼 작동하게 합니다.

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ---
    ### 포물선 닮음 원리 설명
    **포물선은 모두 닮음이다**는 중요한 기하학적 사실입니다. 이는 아무리 다른 모양의 포물선이라도, **적절히 확대/축소하고 이동(평행이동)**시키면 서로 완벽하게 겹쳐질 수 있다는 것을 의미합니다.

    이 도구를 사용하여 다음을 시도해보세요:
    1.  **두 포물선의 `a` 값만 다르게 설정**하고, `확대/축소` 슬라이더를 조절하여 두 포물선을 겹쳐보세요. `a` 값이 0이 아니라면, `a`의 절댓값에 비례하여 포물선의 폭이 결정되는데, 이 `a` 값의 차이를 `확대/축소`로 보정할 수 있습니다.
    2.  **`b`와 `c` 값을 다르게 설정**하여 포물선의 꼭짓점 위치를 바꿔보세요. 그 다음, `x축 이동`과 `y축 이동` 슬라이더를 조절하여 두 포물선의 꼭짓점을 겹쳐보세요.
    3.  이 과정을 통해, 모든 포물선이 단지 **크기와 위치**만 다를 뿐, 근본적인 **형태는 동일하다**는 것을 직관적으로 이해할 수 있을 것입니다.

    이러한 성질은 포물선의 **정의** (한 정점과 한 정직선으로부터 같은 거리에 있는 점들의 자취)에서 비롯되며, 이는 모든 포물선이 하나의 기하학적 형태로 분류될 수 있음을 보여줍니다.
    """)
