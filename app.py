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

# --- 강력한 커스텀 CSS (이미지 디자인 이식) ---
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp { background-color: #121212; }
    
    /* 제목 스타일 */
    h1 { 
        color: white !important; 
        font-weight: 800 !important; 
        font-size: 3rem !important;
        margin-bottom: 40px !important;
        text-align: center;
    }

    /* 버튼 공통 스타일 (박스 크기 및 텍스트) */
    .stButton > button, .stMicRecorder button {
        height: 220px !important;
        width: 100% !important;
        border-radius: 12px !important;
        border: none !important;
        color: white !important;
        margin-bottom: 20px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.5 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* 1. 녹음 박스 (빨강) */
    .stMicRecorder button {
        background-color: #E74C3C !important;
    }
    
    /* 2. 일반 재생 박스 (초록) */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) .stButton > button {
        background-color: #2ECC71 !important;
    }

    /* 3. 역재생 박스 (파랑) */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) .stButton > button {
        background-color: #3498DB !important;
    }

    /* 아이콘 크기 조절 (텍스트 위에 배치) */
    .icon-font { font-size: 50px; margin-bottom: 10px; display: block; }
    .text-font { font-size: 22px; font-weight: bold; display: block; }

    /* 오디오 플레이어 숨기기 */
    audio { display: none !important; }
    
    /* 안내 문구 */
    .info-text { text-align: center; color: white; opacity: 0.5; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 유틸리티 함수 ---
def autoplay_audio(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# --- 사이드바 ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.radio("언어 설정 / Language", ["한국어", "English"], index=0)
    st.markdown("---")
    if st.button("🔄 Reset App"):
        st.session_state.audio_data = None
        st.session_state.reversed_data = None
        st.rerun()

# --- 언어별 텍스트 ---
t = {
    "한국어": {
        "rec_start": "🎤\n녹음하기",
        "rec_stop": "🛑\n녹음 중 (중단)",
        "play": "▶️\n일반 재생",
        "rev": "◀️\n역재생",
        "guide": "빨간색 박스를 눌러 목소리를 기록해보세요."
    },
    "English": {
        "rec_start": "🎤\nStart Recording",
        "rec_stop": "🛑\nRecording (Stop)",
        "play": "▶️\nPlay Recorded",
        "rev": "◀️\nPlay Reverse",
        "guide": "Tap the red box to start recording."
    }
}[lang]

# --- 메인 화면 ---
st.markdown("<h1>Reverse Voice Player</h1>", unsafe_allow_html=True)

# 1. 빨강 박스 (녹음)
audio_result = mic_recorder(
    start_prompt=t["rec_start"],
    stop_prompt=t["rec_stop"],
    key='recorder',
    use_container_width=True
)

if audio_result:
    st.session_state.audio_data = audio_result['bytes']
    audio_seg = AudioSegment.from_file(io.BytesIO(st.session_state.audio_data))
    rev_seg = audio_seg.reverse()
    buf = io.BytesIO()
    rev_seg.export(buf, format="wav")
    st.session_state.reversed_data = buf.getvalue()

# 2. 초록 박스 (일반 재생)
if st.button(t["play"], key="play_btn", use_container_width=True):
    if "audio_data" in st.session_state and st.session_state.audio_data:
        autoplay_audio(st.session_state.audio_data)
    else:
        st.error("먼저 녹음을 해주세요!" if lang=="한국어" else "Please record first!")

# 3. 파랑 박스 (역재생)
if st.button(t["rev"], key="rev_btn", use_container_width=True):
    if "reversed_data" in st.session_state and st.session_state.reversed_data:
        autoplay_audio(st.session_state.reversed_data)
    else:
        st.error("먼저 녹음을 해주세요!" if lang=="한국어" else "Please record first!")

# 가이드 텍스트
if "audio_data" not in st.session_state or not st.session_state.audio_data:
    st.markdown(f"<p class='info-text'>{t['guide']}</p>", unsafe_allow_html=True)
