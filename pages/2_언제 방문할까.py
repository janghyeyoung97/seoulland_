import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# 제목
st.markdown(
    """
    <div style="background-color: #fffacd; padding: 10px; border-radius: 5px;">
        <h1 style="text-align: center;">서울랜드, 언제 방문할까?</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 안내 문구
st.write("### 서울랜드 방문 날짜를 정해봅시다!")
st.write("""
이왕이면 날씨 좋고 사람 적은 날 가서 실컷 노는 게 좋겠죠? 😊
아래 그래프를 보며 가장 좋은 시기를 3개 정도 골라봅시다!
""")

# 데이터 로드 함수
@st.cache_data
def load_data():
    # CSV 파일 로드 (예시 데이터)
    data = pd.read_csv("일일방문자수.csv")
    data["관람객수"] = pd.to_numeric(data["관람객수"], errors="coerce")
    return data

# 데이터 로드
data = load_data()

# 1️⃣ 년도별 월별 관람객수 그래프
st.subheader("1️⃣ 년도별 월별 관람객수 그래프")
selected_year = st.selectbox("Select Year:", data["년도"].unique())
monthly_data = data[data["년도"] == selected_year].groupby("월")["관람객수"].sum()
plt.figure(figsize=(10, 6))
plt.bar(monthly_data.index, monthly_data.values, color="skyblue")
plt.xlabel("Month")  # x축 이름
plt.ylabel("Number of Visitors")  # y축 이름
plt.title(f"Monthly Visitors in {selected_year}")  # 그래프 제목
st.pyplot(plt)

# 2️⃣ 특정 년도와 월의 일별 관람객수 그래프
st.subheader("2️⃣ 특정 년도와 월의 일별 관람객수 그래프")
col1, col2 = st.columns(2)
with col1:
    year_for_daily = st.selectbox("Select Year:", data["년도"].unique(), key="daily_year")
with col2:
    month_for_daily = st.selectbox("Select Month:", sorted(data["월"].unique()), key="daily_month")
daily_data = data[(data["년도"] == year_for_daily) & (data["월"] == month_for_daily)].groupby("일")["관람객수"].sum()
plt.figure(figsize=(10, 6))
plt.plot(daily_data.index, daily_data.values, marker="o", color="green")
plt.xlabel("Day")  # x축 이름
plt.ylabel("Number of Visitors")  # y축 이름
plt.title(f"Daily Visitors in {year_for_daily}, {month_for_daily}")  # 그래프 제목
st.pyplot(plt)

# 3️⃣ 요일별 평균 관람객수 그래프
st.subheader("3️⃣ 요일별 평균 관람객수 그래프")

# 요일 이름을 영어로 변경
weekday_order_kr = ["월", "화", "수", "목", "금", "토", "일"]
weekday_order_en = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

# 데이터를 영어 요일 순서로 재정렬
weekday_data = data.groupby("요일")["관람객수"].mean()
weekday_data = weekday_data.reindex(weekday_order_kr)  # 한국어 요일 순서로 재정렬
weekday_data.index = weekday_order_en  # X축 이름을 영어로 변경

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.bar(weekday_data.index, weekday_data.values, color="orange")
plt.xlabel("Weekday")  # x축 이름
plt.ylabel("Average Number of Visitors")  # y축 이름
plt.title("Average Visitors by Weekday")  # 그래프 제목
st.pyplot(plt)

# 방문 날짜 정하기 가이드
st.subheader("📘 방문 날짜 정하기 가이드")
st.markdown("""
<style>
    .guide-item {
        font-size: 16px;
        margin-bottom: 10px;
    }
    .guide-number {
        font-weight: bold;
        font-size: 18px;
        color: #4CAF50;
    }
</style>
<div class="guide-item"><span class="guide-number">1.</span> 여름방학, 겨울방학에는 방문 불가능.</div>
<div class="guide-item"><span class="guide-number">2.</span> 학교 현장체험학습이니 평일에 방문합니다.</div>
<div class="guide-item"><span class="guide-number">3.</span> 주요 학사 일정 고려하기 (중간고사, 기말고사).</div>
<div class="guide-item"><span class="guide-number">4.</span> 공휴일, 재량휴업일 고려하기.</div>
""", unsafe_allow_html=True)

# 최종 방문 날짜 및 이유 입력 섹션
st.subheader("✏️ 최종 방문 날짜 및 이유")

# 날짜 입력
final_visit_date = st.text_input("선택한 날짜:", placeholder="예: 8월 15일")

# 이유 입력
final_visit_reason = st.text_area(
    "이유:",
    placeholder="선택한 날짜로 정한 이유를 위에서 살펴본 데이터와 정보들을 종합하여 구체적으로 입력하세요.",
    height=150
)

# 제출 버튼
if st.button("최종 입력 완료"):
    if not final_visit_date.strip():
        st.warning("선택한 날짜를 입력해주세요.")
    elif not final_visit_reason.strip():
        st.warning("이유를 입력해주세요.")
    else:
        # 세션 상태에 최종 날짜와 이유 저장
        st.session_state["final_visit_date"] = final_visit_date
        st.session_state["final_visit_reason"] = final_visit_reason
        
        # 성공 메시지
        st.success("최종 방문 날짜와 이유가 저장되었습니다!")
        st.write(f"### 선택한 날짜: {final_visit_date}")
        st.write(f"### 이유: {final_visit_reason}")
