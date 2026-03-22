import streamlit as st
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import io
import base64

# --- 앱 설정 ---
st.set_page_config(
    page_title="Reverse Voice Player", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 사이드바 설정 (언어 선택을 위해 위로 배치) ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.radio("언어 설정 / Language", ["한국어", "English"], index=0)
    st.markdown("---")
    if st.button("🔄 Reset App"):
        st.session_state.audio_data = None
        st.session_state.reversed_data = None
        st.rerun()

# --- 언어별 텍스트 및 타이틀 설정 💡 ---
t = {
    "한국어": {
        "title": "역재생 녹음기",
        "rec_start": "🎤\n녹음하기",
        "rec_stop": "🛑\n녹음 중 (중단)",
        "play": "▶️\n일반 재생",
        "rev": "◀️\n역재생",
        "guide": "빨간색 박스를 눌러 목소리를 기록해보세요."
    },
    "English": {
        "title": "Reverse Voice Player",
        "rec_start": "🎤\nStart Recording",
        "rec_stop": "🛑\nRecording (Stop)",
        "play": "▶️\nPlay Recorded",
        "rev": "◀️\nPlay Reverse",
        "guide": "Tap the red box to start recording."
    }
}[lang]

# --- 초강력 CSS 주입 (박스 강제 고정) 💡 ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #121212; }}
    
    /* 타이틀 스타일 */
    .main-title {{
        color: white !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 40px;
    }}

    /* 버튼 공통 레이아웃 */
    .stButton > button, .stMicRecorder button {{
        height: 220px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: none !important;
        color: white !important;
        font-size: 24px !important;
        font-weight: bold !important;
        white-space: pre-wrap !important;
        line-height: 1.6 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
    }}

    /* 각 박스 전용 색상 💡 */
    /* 1. 녹음 (빨강) */
    .record-wrap .stMicRecorder button {{
        background-color: #E74C3C !important;
    }}
    
    /* 2. 일반재생 (초록) */
    .play-wrap .stButton > button {{
        background-color: #2ECC71 !important;
    }}

    /* 3. 역재생 (파랑) */
    .rev-wrap .stButton > button {{
        background-color: #3498DB !important;
    }}

    /* 지저분한 요소 제거 */
    audio {{ display: none !important; }}
    .info-text {{ text-align: center; color: white; opacity: 0.5; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# --- 메인 화면 출력 ---
st.markdown(f"<h1 class='main-title'>{t['title']}</h1>", unsafe_allow_html=True)

# 1. 빨강 박스 (녹음하기)
st.markdown('<div class="record-wrap">', unsafe_allow_html=True)
audio_result = mic_recorder(
    start_prompt=t["rec_start"],
    stop_prompt=t["rec_stop"],
    key='recorder',
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# 데이터 처리 로직
if audio_result:
    st.session_state.audio_data = audio_result['bytes']
    audio_seg = AudioSegment.from_file(io.BytesIO(st.session_state.audio_data))
    rev_seg = audio_seg.reverse()
    buf = io.BytesIO()
    rev_seg.export(buf, format="wav")
    st.session_state.reversed_data = buf.getvalue()

# 2. 초록 박스 (일반 재생)
st.markdown('<div class="play-wrap">', unsafe_allow_html=True)
if st.button(t["play"], key="play_btn", use_container_width=True):
    if "audio_data" in st.session_state and st.session_state.audio_data:
        b64 = base64.b64encode(st.session_state.audio_data).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/wav;base64,{b64}" type="audio/wav"></audio>', unsafe_allow_html=True)
    else:
        st.error("먼저 녹음을 해주세요!" if lang=="한국어" else "Please record first!")
st.markdown('</div>', unsafe_allow_html=True)

# 3. 파랑 박스 (역재생)
st.markdown('<div class="rev-wrap">', unsafe_allow_html=True)
if st.button(t["rev"], key="rev_btn", use_container_width=True):
    if "reversed_data" in st.session_state and st.session_state.reversed_data:
        b64 = base64.b64encode(st.session_state.reversed_data).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/wav;base64,{b64}" type="audio/wav"></audio>', unsafe_allow_html=True)
    else:
        st.error("먼저 녹음을 해주세요!" if lang=="한국어" else "Please record first!")
st.markdown('</div>', unsafe_allow_html=True)

# 하단 가이드
if "audio_data" not in st.session_state or not st.session_state.audio_data:
    st.markdown(f"<p class='info-text'>{t['guide']}</p>", unsafe_allow_html=True)
