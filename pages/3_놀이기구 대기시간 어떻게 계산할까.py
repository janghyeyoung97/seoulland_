import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# 사이드바: 접속 정보 표시
with st.sidebar:
    st.header("접속 정보")
    if st.session_state.get("student_name"):
        st.success(f"{st.session_state['student_name']} 학생이 접속 중입니다")
        
        # 조 이름이 있을 경우 표시
        if st.session_state.get("team_name"):
            st.info(f"({st.session_state['team_name']}) 놀이공원 이용 계획을 세우는 중입니다!")
        else:
            st.warning("조 이름이 설정되지 않았습니다. '조편성하기'에서 설정해주세요.")
    else:
        st.info("로그인 후 접속 정보가 표시됩니다.")

# 페이지 제목
st.markdown(
    """
    <div style="background-color: #fffacd; padding: 10px; border-radius: 5px;">
        <h1 style="text-align: center;">놀이기구 대기 시간은 어떻게 계산하는걸까?</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 이미지와 설명
st.image("대기시간2.jpg", caption="서울랜드 월드컵과 대기시간 안내판")

st.markdown(
    """
    <p style="font-size: 16px; line-height: 1.6;">
        <b style="color: blue;">월드컵</b>은 서울랜드에서 가장 인기 있는 놀이기구 중 하나로, 
        항상 대기 시간이 길기로 유명합니다.<br><br>
        놀이기구 대기 줄에는 항상 예상 대기 시간이 표시되는데요.<br><br>
        놀이공원에서는 그 대기 시간을 <b style="color: red;">어떻게 알려주는 걸까요?</b>
    </p>
    """,
    unsafe_allow_html=True
)

#구분선
st.markdown(
    """
    <hr style="border-top: 2px dashed #bbb;" />
    """, 
    unsafe_allow_html=True
)


# 실제 데이터 로드
@st.cache_data
def load_queue_data():
    data = pd.read_csv("월드컵데이터.csv", encoding="cp949", header=0, names=["line", "time"])
    data["line"] = pd.to_numeric(data["line"], errors="coerce")
    data["time"] = pd.to_numeric(data["time"], errors="coerce")
    return data

data = load_queue_data()

# 실제 데이터 그래프
st.write("### 🎢 '월드컵'의 줄 길이(line)별 대기시간(time) 그래프")

plt.figure(figsize=(8, 6))
plt.scatter(data["line"], data["time"], color="blue", label="Actual Data")
plt.xlabel("Line Length")  # x축 이름
plt.ylabel("Waiting Time")  # y축 이름
plt.title("Line Length and Waiting Time for 'World Cup'")  # 그래프 제목
plt.grid(True)
plt.legend()
st.pyplot(plt)


# "표로 보기" 버튼
if st.button("표로 보기"):
    # 데이터프레임 복사
    integer_data = data.copy()

    # 결측치(NaN) 처리 - 0으로 대체
    integer_data.fillna(0, inplace=True)
    
    # 데이터 정수 변환
    integer_data["line"] = integer_data["line"].astype(int)
    integer_data["time"] = integer_data["time"].astype(int)
    
    st.write("### 📋 '월드컵' 데이터 표")
    st.table(integer_data)

# 대기시간 일차함수 식 추론하기
st.write("### 📏 대기시간 일차함수 식 추론하기")
st.latex("y = mx + b")

# 사용자의 입력
with st.form("linear_modeling"):
    m = st.number_input("기울기 (m):", step=0.1, format="%.2f", value=0.5)
    b = st.number_input("절편 (b):", step=0.1, format="%.2f", value=0.0)
    submit_model = st.form_submit_button("적합성 계산 및 그래프 그리기")

# 적합도 계산 및 시각화
if submit_model:
    x = data["line"]
    y_actual = data["time"]
    y_pred = m * x + b

    # 적합성 계산 (R²)
    r2 = r2_score(y_actual, y_pred)
    st.success(f"입력한 함수의 적합 정도 (R²): {r2:.2f}")

    # 데이터와 사용자가 입력한 1차 함수 시각화
    # 데이터와 사용자가 입력한 1차 함수 시각화
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y_actual, label="Actual Data", color="blue")  # 범례를 영어로 변경
    plt.plot(x, y_pred, label=f"User Function: y = {m:.2f}x + {b:.2f}", color="red")  # 범례 수정
    plt.xlabel("Line Length")  # x축 이름
    plt.ylabel("Waiting Time")  # y축 이름
    plt.title("Comparison of Actual Data and User Function")  # 그래프 제목
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

#구분선
st.markdown(
    """
    <hr style="border-top: 2px dashed #bbb;" />
    """, 
    unsafe_allow_html=True
)



# 추가 섹션: 놀이공원 대기시간 설정 방식
st.subheader("🎢 놀이공원 대기시간은 어떻게 설정할까?")
st.markdown("""
놀이공원에서는 놀이기구별 대기시간을 설정하기 위해 다양한 데이터를 활용합니다.
'월드컵' 놀이기구의 대기시간을 예상하기 위해 필요한 자료는 다음과 같습니다:
""")

# 정보 제공
st.markdown("""
- 줄 길이 **1m당 3명**의 사람이 서있다고 가정합니다.
- '월드컵' 놀이기구는 **1회 탑승 인원 40명**입니다.
- 한번 타고 내릴 때 평균 **4분의 시간이 소요**됩니다.
""")

st.write("위의 자료를 바탕으로 '월드컵' 놀이기구 대기시간에 대한 일차함수 식을 세워보세요!")
# 추가 식 입력 섹션
st.write("### 📝 대기시간 일차함수 식 입력")
with st.form("unique_park_modeling"):  # 'unique_' 접두사를 추가하여 key를 고유하게 설정
    m_custom = st.number_input("기울기 (m):", step=0.1, format="%.2f", value=0.1, key="custom_m")
    b_custom = st.number_input("절편 (b):", step=0.1, format="%.2f", value=0.0, key="custom_b")
    method_m = st.text_area(
        "기울기를 구한 방법:",
        placeholder="기울기를 구한 과정을 간단히 작성해주세요.",
        height=100,
        key="method_m"
    )
    method_b = st.text_area(
        "절편을 구한 방법:",
        placeholder="절편을 구한 과정을 간단히 작성해주세요.",
        height=100,
        key="method_b"
    )
    submit_custom_model = st.form_submit_button("식 저장 및 확인")

# 결과 출력
if submit_custom_model:
    if not method_m.strip():
        st.warning("기울기를 구한 방법을 입력해주세요.")
    elif not method_b.strip():
        st.warning("절편을 구한 방법을 입력해주세요.")
    else:
        st.success("대기시간 식이 저장되었습니다!")
        st.write(f"### 입력된 함수:")
        st.latex(f"y = {m_custom:.2f}x + {b_custom:.2f}")

        # 입력된 기울기와 절편 구한 방법 표시
        st.write("#### 기울기를 구한 방법:")
        st.write(method_m)

        st.write("#### 절편을 구한 방법:")
        st.write(method_b)

        # 그래프 시각화
        st.write("### 🎨 대기시간 예상 그래프")
        x_custom = np.linspace(0, 100, 100)  # 0m ~ 100m 줄 길이
        y_custom = m_custom * x_custom + b_custom

        plt.figure(figsize=(8, 6))
        plt.plot(x_custom, y_custom, color="green", label=f"y = {m_custom:.2f}x + {b_custom:.2f}")
        plt.xlabel("Line Length")  # x축 이름
        plt.ylabel("Waiting Time")  # y축 이름
        plt.title("Relationship Between Line Length and Waiting Time")  # 그래프 제목
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

