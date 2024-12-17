import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="서울랜드 방문 계획", layout="centered")

# 세션 상태 초기화
if "student_name" not in st.session_state:
    st.session_state["student_name"] = None

# 사이드바: 접속 정보 표시
with st.sidebar:
    st.header("접속 정보")
    if st.session_state["student_name"]:
        st.success(f"{st.session_state['student_name']} 학생이 접속 중입니다")
    else:
        st.info("로그인 후 접속 정보가 표시됩니다.")

# 제목 (중앙 정렬, 무지개 구분선 포함)
st.header('🎢 서울랜드 :blue[방문 도우미] 플랫폼', divider="rainbow")

# 이미지 추가
st.image("서울랜드지도.jpg")

# 로그인 입력
st.subheader("😊 도우미 입장! 🎉")
with st.form("로그인"):
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("이름", placeholder="이름을 입력하세요", key="name_input")
    with col2:
        student_id = st.text_input("학번", placeholder="학번을 입력하세요", key="id_input")
    
    submitted = st.form_submit_button("🚪 입장하기")

# 로그인 동작
if submitted:
    if not student_name or not student_id:
        st.warning("이름과 학번을 모두 입력해주세요.")
    else:
        st.success(f"{student_name} 학생 환영합니다!")
        
        # 세션 상태에 사용자 정보 저장
        st.session_state["student_name"] = student_name
        
        # 진행 바
        progress_text = "로그인 중입니다..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        
        st.success("로그인 성공! 다음 페이지로 이동합니다.")
        
        # 페이지 이동
        st.switch_page("pages/1_조편성하기.py")
