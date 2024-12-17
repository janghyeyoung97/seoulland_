import streamlit as st

# 페이지 설정
st.set_page_config(page_title="조편성하기", layout="centered")

# 세션 상태 초기화
if "team_name" not in st.session_state:
    st.session_state["team_name"] = None

if "team_members" not in st.session_state:
    st.session_state["team_members"] = None

# 사이드바: 접속 정보 표시
with st.sidebar:
    st.header("접속 정보")
    if st.session_state.get("student_name"):
        st.success(f"{st.session_state['student_name']} 학생이 접속 중입니다")
        if st.session_state.get("team_name"):
            st.info(f"({st.session_state['team_name']}) 놀이공원 이용 계획을 세우는 중입니다!")
    else:
        st.info("로그인 후 접속 정보가 표시됩니다.")

# 페이지 제목
st.markdown(
    """
    <div style="background-color: #fffacd; padding: 10px; border-radius: 5px;">
        <h1 style="text-align: center;">조편성하기</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 설문조사 섹션
st.subheader("🎢 설문조사")
with st.form("survey_form"):
    # 질문 1: 놀이기구 타는 것을 좋아해?
    q1 = st.radio(
        "1. 놀이기구 타는 것을 좋아해?",
        ("매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다")
    )
    
    # 질문 2: 무서운 놀이기구 잘 타?
    q2 = st.radio(
        "2. 무서운 놀이기구 잘 타?",
        ("매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다")
    )
    
    # 질문 3: 서울랜드 가서 꼭 타고 싶은 놀이기구는?
    q3 = st.selectbox(
        "3. 서울랜드 가서 꼭 타고 싶은 놀이기구는?",
        ("바이킹", "롤러코스터", "귀신의 집", "월드컵")
    )
    
    # 질문 4: 놀이기구 줄 오래 서는거 어때?
    q4 = st.radio(
        "4. 놀이기구 줄 오래 서는거 어때?",
        ("아주 괜찮아", "괜찮아", "보통이다", "싫어", "너무 싫어")
    )

    # 설문조사 제출 버튼
    survey_submitted = st.form_submit_button("제출")

# 설문조사 제출 후 데이터 표시
if survey_submitted:
    st.success("설문조사가 제출되었습니다!")
    st.write("### 설문조사 결과:")
    st.write(f"1. 놀이기구 타는 것을 좋아해? **{q1}**")
    st.write(f"2. 무서운 놀이기구 잘 타? **{q2}**")
    st.write(f"3. 꼭 타고 싶은 놀이기구: **{q3}**")
    st.write(f"4. 놀이기구 줄 오래 서는거 어때? **{q4}**")
    st.markdown("### 🌟 나와 같은 취향의 친구를 찾아 조를 구성해봅시다!")

# 추가 입력 섹션
st.subheader("📝 조 이름과 구성원 입력")
with st.form("team_form"):
    team_name = st.text_input("조 이름:", placeholder="예: 놀이기구 마스터 조")
    team_members = st.text_area("조 구성원:", placeholder="예: 김철수, 이영희, 박민수")
    
    # 추가 제출 버튼
    team_submitted = st.form_submit_button("조 구성 완료")

# 팀 이름과 구성원 입력 후 사이드바 업데이트
if team_submitted:
    if not team_name or not team_members.strip():
        st.warning("조 이름과 구성원을 모두 입력해주세요.")
    else:
        st.success(f"조 이름: {team_name}, 구성원: {team_members}")
        
        # 세션 상태에 저장
        st.session_state["team_name"] = team_name
        st.session_state["team_members"] = team_members
        
        st.info("사이드바에 팀 정보가 업데이트되었습니다!")
