import streamlit as st
from streamlit_mic_recorder import mic_recorder
import numpy as np
import io
import wave

# --- 앱 설정 및 스타일 ---
st.set_page_config(page_title="⏪ 리버스 보이스", layout="centered")

st.markdown("""
<style>
    .block {
        border-radius: 15px;
        padding: 30px;
        margin: 10px 0;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
    }
    .red { background-color: #E74C3C; }
    .green { background-color: #2ECC71; }
    .blue { background-color: #3498DB; }
    /* 오디오 플레이어 스타일 숨기기 (깔끔하게) */
    audio { width: 100%; margin-top: 10px; }
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
    # 2. 정방향 재생 섹션 (Green Block)
    st.markdown("---")
    st.markdown("<div class='block green'>▶️ Play Recorded</div>", unsafe_allow_html=True)
    st.audio(audio['bytes'], format='audio/wav')

    # 3. 역방향 처리 로직
    audio_bio = io.BytesIO(audio['bytes'])
    with wave.open(audio_bio, 'rb') as wav_file:
        params = wav_file.getparams()
        frames = wav_file.readframes(params.nframes)
        audio_array = np.frombuffer(frames, dtype=np.int16)
        # 💡 핵심 기능: 데이터를 거꾸로 뒤집기!
        reversed_array = audio_array[::-1]
        
        output_bio = io.BytesIO()
        with wave.open(output_bio, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(reversed_array.tobytes())

    # 4. 역방향 재생 섹션 (Blue Block)
    st.markdown("---")
    st.markdown("<div class='block blue'>⏪ Play Reverse</div>", unsafe_allow_html=True)
    st.audio(output_bio.getvalue(), format='audio/wav')
    
    st.success("✨ 목소리가 거꾸로 뒤집혔습니다! 신기하죠?")

else:
    st.info("💡 위의 빨간색 버튼 영역에서 '녹음 시작하기'를 눌러보세요.")

# --- 사이드바 설정 (달력 앱의 감성 유지) ---
with st.sidebar:
    st.header("⚙️ 앱 설정")
    st.write("1️⃣ **사용 방법**")
    st.caption("녹음 후 초록색 버튼은 원래 소리, 파란색 버튼은 거꾸로 된 소리를 들려줍니다.")
    st.write("---")
    st.write("2️⃣ **파일 정보**")
    if audio:
        st.write(f"📏 녹음 크기: {len(audio['bytes'])/1024:.1f} KB")
    else:
        st.write("녹음된 파일이 없습니다.")
    st.write("---")
    st.caption("🚀 최종 수정: 2026.03.23")
