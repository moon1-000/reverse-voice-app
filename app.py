import streamlit as st
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import io

# --- 앱 설정 ---
st.set_page_config(page_title="⏪ 리버스 보이스", layout="centered")

st.markdown("""
<style>
    .block { border-radius: 15px; padding: 30px; margin: 10px 0; text-align: center; color: white; font-weight: bold; font-size: 20px; }
    .red { background-color: #E74C3C; }
    .green { background-color: #2ECC71; }
    .blue { background-color: #3498DB; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🎙️ 리버스 보이스 플레이어</h2>", unsafe_allow_html=True)
st.write("---")

# --- 1. 녹음 섹션 (Red Block) ---
st.markdown("<div class='block red'>🎤 Start Recording</div>", unsafe_allow_html=True)
audio = mic_recorder(
    start_prompt="녹음 시작하기",
    stop_prompt="녹음 멈추기",
    key='recorder'
)

if audio:
    # 2. 오디오 처리 (Pydub 활용) 💡 어떤 형식이든 WAV로 변환해줍니다.
    audio_bytes = audio['bytes']
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # --- 2. 정방향 재생 섹션 (Green Block) ---
    st.markdown("---")
    st.markdown("<div class='block green'>▶️ Play Recorded</div>", unsafe_allow_html=True)
    st.audio(audio_bytes)

    # --- 3. 역방향 처리 섹션 (Blue Block) ---
    # 💡 한 줄로 소리 뒤집기!
    reversed_audio = audio_segment.reverse()
    
    # 다시 플레이어로 내보내기 위해 변환
    buf = io.BytesIO()
    reversed_audio.export(buf, format="wav")
    
    st.markdown("---")
    st.markdown("<div class='block blue'>⏪ Play Reverse</div>", unsafe_allow_html=True)
    st.audio(buf.getvalue())
    
    st.success("✨ 목소리를 성공적으로 뒤집었습니다!")

else:
    st.info("💡 빨간색 버튼을 눌러 녹음을 시작해보세요.")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 앱 정보")
    st.caption("🚀 버전: V3.0 (모든 브라우저 지원)")
    st.caption("최종 수정: 2026.03.23")
