import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 사이드바: 접속 정보 표시
with st.sidebar:
    st.header("접속 정보")
    if st.session_state.get("student_name"):
        st.success(f"{st.session_state['student_name']} 학생이 접속 중입니다")
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
        <h1 style="text-align: center;">어떻게 방문할까?</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 1. '어트랙션정보.csv' 파일 로드 및 표시
st.subheader("🎢 어트랙션 정보")
@st.cache_data
def load_attraction_data():
    return pd.read_csv("어트랙션정보.csv")

attraction_data = load_attraction_data()
st.write("아래는 어트랙션별 탑승 인원 및 소요 시간 정보입니다.")
st.table(attraction_data)

# 2. 학생들이 어트랙션 4개 선택
st.subheader("📝 어트랙션 선택")
selected_attractions = st.multiselect(
    "탑승하고 싶은 어트랙션 4개를 선택하세요:",
    attraction_data["어트랙션"],
    max_selections=4
)

if len(selected_attractions) == 4:
    st.success(f"선택한 어트랙션: {', '.join(selected_attractions)}")
else:
    st.warning("어트랙션을 4개 선택해주세요!")

# 3. 함수 생성하기와 시뮬레이션
if "user_functions" not in st.session_state:
    st.session_state.user_functions = []

if "simulation_active" not in st.session_state:
    st.session_state.simulation_active = False

if "simulation_done" not in st.session_state:
    st.session_state.simulation_done = False

if len(selected_attractions) == 4:
    st.subheader("📏 대기시간 일차함수 만들기")
    st.write(
        """
        선택한 놀이기구별 대기시간 일차함수를 완성해봅시다! 
        아래 입력하고 함수가 맞는지 확인해보세요! 기울기는 소숫점 둘쨋자리까지 입력합니다! 😊
        """
    )

    # 입력 칸 생성 (4개 놀이기구 한 번에)
    input_data = {}
    for attraction in selected_attractions:
        st.write(f"### {attraction}의 대기시간 함수 입력")
        col1, col2 = st.columns(2)
        with col1:
            m = st.number_input(f"{attraction}의 기울기 (m):", step=0.01, format="%.2f", key=f"{attraction}_m")
        with col2:
            b = st.number_input(f"{attraction}의 절편 (b):", step=0.01, format="%.2f", key=f"{attraction}_b")
        input_data[attraction] = {"m": m, "b": b}

    # 함수 생성 버튼
    if st.button("함수 생성하기"):
        st.session_state.user_functions.clear()
        incorrect_attractions = []

        for attraction, values in input_data.items():
            # 어트랙션 정보 가져오기
            attraction_info = attraction_data[attraction_data["어트랙션"] == attraction].iloc[0]
            capacity = attraction_info["탑승인원(명)"]
            ride_time = attraction_info["탑승시간(분)"]

            # 실제 함수 계산
            actual_m = round(3 / capacity * ride_time, 2)  # 둘째 자리 반올림
            actual_b = round(ride_time, 2)  # 둘째 자리 반올림

            if round(values["m"], 2) == actual_m and round(values["b"], 2) == actual_b:
                st.session_state.user_functions.append({"어트랙션": attraction, "기울기": values["m"], "절편": values["b"]})
            else:
                incorrect_attractions.append(attraction)

        if len(incorrect_attractions) == 0:
            st.success("모두 정확합니다!")
            st.session_state.simulation_active = True

            # 완성된 일차함수 표시
            st.write("### 완성된 일차함수:")
            for idx, func in enumerate(st.session_state.user_functions, start=1):
                st.markdown(f"{idx}. **{func['어트랙션']}**: \( y = {func['기울기']}x + {func['절편']} \)")
        else:
            st.error(f"{', '.join(incorrect_attractions)}가 틀렸습니다. 다시 확인해주세요!")

# 4. 대기시간 시뮬레이션 해보기
if st.session_state.simulation_active:
    st.subheader("🎯 대기시간 시뮬레이션 해보기")
    st.write("""
        총 1000명의 방문객이 있다고 가정하고, 이들을 4개의 놀이기구에 배치해보세요!
        인원수를 입력하면 예상 대기시간을 계산해줍니다.
    """)

    total_visitors = 1000  # 방문객 수
    visitor_distribution = {}
    total_assigned = 0

    for func in st.session_state.user_functions:
        attraction = func["어트랙션"]
        visitor_distribution[attraction] = st.number_input(
            f"{attraction}에 배정할 인원 수:",
            min_value=0,
            max_value=total_visitors,
            step=1,
            key=f"{attraction}_visitors"
        )
        total_assigned += visitor_distribution[attraction]

    remaining_visitors = total_visitors - total_assigned
    if remaining_visitors < 0:
        st.error("배정한 인원이 1000명을 초과했습니다. 다시 확인해주세요!")
    else:
        st.info(f"남은 인원: {remaining_visitors}명")

    # 결과 확인 버튼
    if st.button("시뮬레이션 결과 확인"):
        if remaining_visitors > 0:
            st.warning("모든 인원을 배정해야 시뮬레이션 결과를 볼 수 있습니다!")
        else:
            st.success("시뮬레이션 결과:")
            st.write("각 놀이기구의 예상 대기시간을 아래에서 확인하세요!")

            # 시뮬레이션 결과 저장
            simulation_results = {}
            for func in st.session_state.user_functions:
                attraction = func["어트랙션"]
                m = func["기울기"]
                b = func["절편"]
                queue_length = visitor_distribution[attraction] / 3
                wait_time = m * queue_length + b
                simulation_results[attraction] = wait_time

            # 세션 상태에 결과 저장
            st.session_state.simulation_results = simulation_results

    # 결과 표시
    if "simulation_results" in st.session_state:
        simulation_results = st.session_state.simulation_results

        # 번호와 예상 대기시간 표시
        for idx, (attraction, wait_time) in enumerate(simulation_results.items(), start=1):
            st.markdown(f"{idx}. **{attraction}**: 예상 대기시간 **{wait_time:.2f}분**")

        st.subheader("📊 예상 대기시간 그래프")
        attractions = list(range(1, len(simulation_results) + 1))  # 1, 2, 3, 4
        times = list(simulation_results.values())

        # 그래프 그리기
        plt.figure(figsize=(8, 5))
        plt.bar(attractions, times)
        plt.title("Expected Waiting Time by Attraction")
        plt.xlabel("Attraction Number")
        plt.ylabel("Expected Waiting Time (minutes)")
        plt.xticks(attractions)  # x축에 번호만 표시
        st.pyplot(plt)

        # 시뮬레이션 완료 상태 설정
        st.session_state.simulation_done = True

# 5. 동선 결정 및 서울랜드 지도 표시
if st.session_state.simulation_done:
    st.subheader("🗺️ 서울랜드 동선 결정")
    st.write("""
        시뮬레이션에서 살펴본 대기시간과 동선을 고려하여 
        서울랜드에서 탑승할 어트랙션의 순서를 생각해보고 
        추천 동선을 제시해봅시다.
    """)
    
    # 서울랜드 지도 표시
    st.image("서울랜드지도.jpg", caption="서울랜드 지도")
    
   # 사용자 입력: 어트랙션 순서 결정
    user_order = st.text_area(
    "어트랙션 순서 결정 (추천 동선):",
    placeholder="예: 롤러코스터 -> 바이킹 -> 귀신의 집 -> 월드컵"
    )

    # 동선 저장 버튼
    if st.button("동선 저장"):
     if user_order.strip():  # 입력이 비어 있지 않은 경우
        st.session_state["user_order"] = user_order  # 세션 상태에 저장
        st.success("동선이 저장되었습니다!")
        st.write("### 결정한 동선:")
        st.write(user_order)
    else:
        st.warning("동선을 입력해주세요!")


