import streamlit as st
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import io

# --- 앱 기본 설정 ---
st.set_page_config(
    page_title="Reverse Voice Player", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 커스텀 CSS (색상 박스 및 레이아웃) ---
st.markdown("""
<style>
    .stApp { background-color: #121212; }
    h1 { color: white !important; text-align: center; font-weight: 800; }
    
    /* 색상 박스 스타일 */
    .color-box {
        height: 120px;
        width: 100%;
        border-radius: 10px 10px 0 0;
        margin-top: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
    }
    .bg-red { background-color: #E74C3C; }
    .bg-green { background-color: #2ECC71; }
    .bg-blue { background-color: #3498DB; }

    /* 위젯이 들어가는 하단 박스 */
    .widget-container {
        background-color: #222;
        padding: 20px;
        border-radius: 0 0 10px 10px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* 오디오 플레이어 반전 (다크모드 최적화) */
    audio { width: 100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5); }
</style>
""", unsafe_allow_html=True)

# --- 사이드바 설정 ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.radio("언어 설정 / Language", ["한국어", "English"], index=0)
    st.markdown("---")
    if st.button("🔄 Reset App"):
        st.session_state.clear()
        st.rerun()

# --- 언어별 텍스트 ---
t = {
    "한국어": {
        "title": "역재생 녹음기",
        "red_box": "1. 목소리 녹음",
        "green_box": "2. 일반 재생",
        "blue_box": "3. 역방향 재생",
        "rec_start": "녹음하기",
        "rec_stop": "녹음 중... (클릭 시 완료)",
        "play_guide": "녹음 후 재생 바가 나타납니다.",
        "error": "먼저 녹음을 해주세요!"
    },
    "English": {
        "title": "Reverse Voice Player",
        "red_box": "1. Record Voice",
        "green_box": "2. Normal Play",
        "blue_box": "3. Reverse Play",
        "rec_start": "Start Recording",
        "rec_stop": "Recording... (Click to Finish)",
        "play_guide": "Audio player will appear after recording.",
        "error": "Please record first!"
    }
}[lang]

# --- 메인 화면 ---
st.markdown(f"<h1>{t['title']}</h1>", unsafe_allow_html=True)

# --- SECTION 1: RED (Record) ---
st.markdown(f"<div class='color-box bg-red'>{t['red_box']}</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-container'>", unsafe_allow_html=True)
    audio_result = mic_recorder(
        start_prompt=t["rec_start"],
        stop_prompt=t["rec_stop"],
        key='recorder',
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# 데이터 처리
if audio_result:
    st.session_state.audio_bytes = audio_result['bytes']
    audio_seg = AudioSegment.from_file(io.BytesIO(st.session_state.audio_bytes))
    
    # 역재생 생성
    rev_seg = audio_seg.reverse()
    buf = io.BytesIO()
    rev_seg.export(buf, format="wav")
    st.session_state.reversed_bytes = buf.getvalue()

# --- SECTION 2: GREEN (Normal Play) ---
st.markdown(f"<div class='color-box bg-green'>{t['green_box']}</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-container'>", unsafe_allow_html=True)
    if "audio_bytes" in st.session_state:
        st.audio(st.session_state.audio_bytes, format="audio/wav")
    else:
        st.caption(t["play_guide"])
    st.markdown("</div>", unsafe_allow_html=True)

# --- SECTION 3: BLUE (Reverse Play) ---
st.markdown(f"<div class='color-box bg-blue'>{t['blue_box']}</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='widget-container'>", unsafe_allow_html=True)
    if "reversed_bytes" in st.session_state:
        st.audio(st.session_state.reversed_bytes, format="audio/wav")
    else:
        st.caption(t["play_guide"])
    st.markdown("</div>", unsafe_allow_html=True)
