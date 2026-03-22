import streamlit as st
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import io
import os

# --- 앱 설정 ---
# 💡 initial_sidebar_state="collapsed"로 설정하여 사이드바를 기본으로 숨깁니다.
st.set_page_config(
    page_title="⏪ 리버스 보이스", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- 커스텀 CSS (디자인 입히기) ---
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp { background-color: #121212; }
    
    /* 사이드바 어둡게 */
    section[data-testid="stSidebar"] { background-color: #1E1E1E; }
    
    /* 블록 공통 스타일 */
    .block-label {
        padding: 40px;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: -10px;
    }
    
    /* 색상 정의 */
    .red { background-color: #E74C3C; border-radius: 15px 15px 0 0; }
    .green { background-color: #2ECC71; border-radius: 15px 15px 0 0; }
    .blue { background-color: #3498DB; border-radius: 15px 15px 0 0; }
    
    /* 실제 버튼/위젯이 들어가는 하단 영역 */
    .widget-box {
        background-color: #222;
        padding: 20px;
        border-radius: 0 0 15px 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* 오디오 플레이어 스타일 */
    audio { width: 100%; filter: invert(100%); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: white;'>🎙️ 리버스 보이스 플레이어</h2>", unsafe_allow_html=True)
st.write("---")

# --- 1. 녹음 섹션 (Red) ---
st.markdown("<div class='block-label red'>🎤 Start Recording</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-box'>", unsafe_allow_html=True)
    # 💡 에러의 원인이었던 css 파라미터를 삭제했습니다.
    audio = mic_recorder(
        start_prompt="녹음 시작하기",
        stop_prompt="녹음 멈추기",
        key='recorder'
    )
    st.markdown("</div>", unsafe_allow_html=True)

if audio:
    # 오디오 데이터 처리 (Pydub 활용)
    audio_bytes = audio['bytes']
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # --- 2. 정방향 재생 섹션 (Green) ---
    st.markdown("<div class='block-label green'>▶️ Play Recorded</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='widget-box'>", unsafe_allow_html=True)
        st.audio(audio_bytes)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 3. 역방향 처리 및 재생 섹션 (Blue) ---
    reversed_audio = audio_segment.reverse()
    buf = io.BytesIO()
    reversed_audio.export(buf, format="wav")
    
    st.markdown("<div class='block-label blue'>⏪ Play Reverse</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='widget-box'>", unsafe_allow_html=True)
        st.audio(buf.getvalue())
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.success("✨ 목소리를 성공적으로 뒤집었습니다!")

else:
    st.info("💡 위쪽 빨간색 블록의 버튼을 눌러 녹음을 시작하세요.")

# --- 사이드바 (숨겨져 있다가 ☰ 누르면 나타남) ---
with st.sidebar:
    st.header("⚙️ 앱 설정")
    st.write("사이드바가 깔끔하게 숨겨졌습니다!")
    st.markdown("---")
    if st.button("🔄 모두 기본값으로"):
        st.rerun()
    st.caption("🚀 최종 수정: 2026.03.23.01.20")
