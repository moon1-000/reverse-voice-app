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

# --- 커스텀 CSS (이미지 1 감성 구현) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; }
    
    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] { background-color: #1E1E1E; }
    
    /* 텍스트 스타일 */
    h1, h2, h3, p { color: white !important; font-family: 'Pretendard', sans-serif; }

    /* 블록 디자인 (박스 자체를 버튼처럼 보이게) */
    .stButton > button {
        border-radius: 0px !important;
        border: none !important;
        height: 200px !important;
        width: 100% !important;
        color: white !important;
        font-size: 26px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }

    /* 각 색상 버튼 테마 */
    /* 빨간색 녹음 버튼 */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button {
        background-color: #E74C3C !important;
    }
    /* 초록색 재생 버튼 */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button {
        background-color: #2ECC71 !important;
    }
    /* 파란색 역재생 버튼 */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button {
        background-color: #3498DB !important;
    }

    /* 재생 슬라이더 및 기본 오디오 플레이어 숨기기 💡 */
    audio { display: none !important; }
    
    /* 마이크 레코더 기본 버튼 스타일 강제 수정 💡 */
    .stMicRecorder button {
        background-color: #E74C3C !important;
        height: 200px !important;
        width: 100% !important;
        border-radius: 0px !important;
        font-size: 26px !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 상태 관리 및 오디오 재생 함수 ---
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'reversed_data' not in st.session_state:
    st.session_state.reversed_data = None

def autoplay_audio(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# --- 사이드바: 설정 ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.radio("Language / 언어 설정", ["한국어", "English"], index=0)
    st.markdown("---")
    if st.button("🔄 Reset App"):
        st.session_state.audio_data = None
        st.session_state.reversed_data = None
        st.rerun()
    st.caption("🚀 최종 수정: 2026.03.23.04.55")

# --- 메인 화면 ---
st.markdown("<h1 style='text-align: center;'>Reverse Voice Player</h1>", unsafe_allow_html=True)
st.write("")

# 언어별 텍스트 설정 💡
t = {
    "한국어": {
        "rec_start": "녹음하기",
        "rec_stop": "녹음 중 (클릭 시 중단)",
        "play": "일반 재생",
        "rev": "역재생",
        "done": "녹음 완료"
    },
    "English": {
        "rec_start": "Start Recording",
        "rec_stop": "Recording (Click to Stop)",
        "play": "Play Recorded",
        "rev": "Play Reverse",
        "done": "Recording Complete"
    }
}[lang]

# --- 1. 빨강 박스: 녹음 (Start Recording) ---
# mic_recorder의 텍스트를 기획안대로 동적으로 변경
audio_result = mic_recorder(
    start_prompt=t["rec_start"],
    stop_prompt=t["rec_stop"],
    key='recorder',
    use_container_width=True
)

if audio_result:
    st.session_state.audio_data = audio_result['bytes']
    # Pydub으로 소리 뒤집기 처리
    audio_seg = AudioSegment.from_file(io.BytesIO(st.session_state.audio_data))
    rev_seg = audio_seg.reverse()
    buf = io.BytesIO()
    rev_seg.export(buf, format="wav")
    st.session_state.reversed_data = buf.getvalue()
    st.toast(t["done"])

# --- 2. 초록 박스: 일반 재생 (Play Recorded) ---
if st.button(t["play"], use_container_width=True):
    if st.session_state.audio_data:
        autoplay_audio(st.session_state.audio_data)
    else:
        st.warning("먼저 녹음을 해주세요!" if lang=="한국어" else "Please record first!")

# --- 3. 파랑 박스: 역재생 (Play Reverse) ---
if st.button(t["rev"], use_container_width=True):
    if st.session_state.reversed_data:
        autoplay_audio(st.session_state.reversed_data)
    else:
        st.warning("먼저 녹음을 해주세요!" if lang=="한국어" else "Please record first!")

# 하단 안내 텍스트
if not st.session_state.audio_data:
    st.markdown(f"<p style='text-align: center; opacity: 0.6;'>{'빨간색 박스를 눌러 목소리를 기록해보세요.' if lang=='한국어' else 'Tap the red box to start recording.'}</p>", unsafe_allow_html=True)
