import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import tempfile
import os

# 페이지 설정
st.set_page_config(page_title="놀이공원 이용 계획 보고서", layout="wide")

# 사이드바: 접속 정보 표시
with st.sidebar:
    st.header("접속 정보")
    if st.session_state.get("student_name"):
        st.success(f"{st.session_state['student_name']} 학생이 접속 중입니다")
        if st.session_state.get("team_name"):
            st.info(f"({st.session_state['team_name']}) 놀이공원 이용 계획 보고서를 작성 중입니다!")
        else:
            st.warning("조 이름이 설정되지 않았습니다. '조편성하기'에서 설정해주세요.")
    else:
        st.info("로그인 후 접속 정보가 표시됩니다.")

# 제목
st.markdown(
    """
    <div style="background-color: #e6f7ff; padding: 10px; border-radius: 5px;">
        <h1 style="text-align: center;">놀이공원 이용 계획 보고서</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("이 보고서는 이전 페이지에서 입력된 데이터와 결과를 종합하여 만들어집니다.")

# 보고서 데이터 준비
team_name = st.session_state.get("team_name", "미입력")
team_members = st.session_state.get("team_members", "미입력")
final_visit_date = st.session_state.get("final_visit_date", "미입력")
final_visit_reason = st.session_state.get("final_visit_reason", "미입력")
user_order = st.session_state.get("user_order", "미입력")

# 보고서 내용 표시
st.subheader("📋 보고서 내용")

# 1️⃣ 조 정보
st.write("### 1️⃣ 조 정보")
st.write(f"- **조 이름**: {team_name}")
st.write(f"- **조 구성원**: {team_members}")

# 2️⃣ 추천 방문 시기
st.write("### 2️⃣ 추천 방문 시기")
st.write(f"- **최종 방문 날짜**: {final_visit_date}")
st.write(f"- **방문 이유**: {final_visit_reason}")

# 3️⃣ 추천 동선
st.write("### 3️⃣ 추천 동선")
st.write(f"- **결정한 동선**: {user_order}")

# PDF 생성 함수
def create_pdf():
    # 임시 파일 생성
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    # 폰트 등록 (한글 폰트 설정)
    font_path = "NotoSansKR-Regular.ttf"  # 폰트 경로
    if not os.path.exists(font_path):
        st.error("한글 폰트 파일이 존재하지 않습니다. 'NotoSansKR-Regular.ttf'를 프로젝트 폴더에 추가해주세요.")
        return None

    pdfmetrics.registerFont(TTFont('NotoSans', font_path))

    # PDF 생성
    c = canvas.Canvas(temp_file.name, pagesize=A4)
    c.setFont("NotoSans", 18)
    c.drawString(100, 800, "놀이공원 이용 계획 보고서")

    # 조 정보
    c.setFont("NotoSans", 12)
    c.drawString(100, 770, "1. 조 정보")
    c.drawString(120, 750, f"조 이름: {team_name}")
    c.drawString(120, 730, f"조 구성원: {team_members}")

    # 추천 방문 시기
    c.drawString(100, 700, "2. 추천 방문 시기")
    c.drawString(120, 680, f"최종 방문 날짜: {final_visit_date}")
    c.drawString(120, 660, f"방문 이유: {final_visit_reason}")

    # 추천 동선
    c.drawString(100, 630, "3. 추천 동선")
    c.drawString(120, 610, f"결정한 동선: {user_order}")

    # 저장 후 반환
    c.save()
    return temp_file.name

# PDF 다운로드 버튼
if st.button("📄 보고서 PDF 다운로드"):
    pdf_path = create_pdf()
    if pdf_path:
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 PDF 다운로드",
                data=pdf_file,
                file_name="놀이공원_이용_계획_보고서.pdf",
                mime="application/pdf"
            )
        os.unlink(pdf_path)  # 임시 파일 삭제
