import streamlit as st
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment
import io
import os
import urllib.request

# --- 폰트 및 데이터 로직 (V19) ---
def get_font(font_option, uploaded_font, size, lang, force_bold=False):
    if uploaded_font is not None:
        try: return ImageFont.truetype(io.BytesIO(uploaded_font.getvalue()), size)
        except: pass
    font_urls = {
        "나눔고딕": "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf",
        "나눔고딕_Bold": "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf",
        "바탕체": "https://github.com/google/fonts/raw/main/ofl/nanummyeongjo/NanumMyeongjo-Regular.ttf",
        "바탕체_Bold": "https://github.com/google/fonts/raw/main/ofl/nanummyeongjo/NanumMyeongjo-Bold.ttf"
    }
    key = font_option if font_option not in ["Arial", "맑은 고딕"] else "나눔고딕"
    if force_bold: key += "_Bold"
    file_name = f"{key}.ttf"
    if not os.path.exists(file_name):
        try: urllib.request.urlretrieve(font_urls.get(key, font_urls["나눔고딕"]), file_name)
        except: return ImageFont.load_default()
    return ImageFont.truetype(file_name, size)

# --- UI 레이아웃 ---
st.set_page_config(page_title="⏪ 리버스 보이스", layout="centered")

# 💡 커스텀 CSS 정의 (image_1.png 감성)
st.markdown("""
<style>
    /* 전체 앱 배경색 */
    .stApp {
        background-color: #121212;
    }
    
    /* 사이드바 스타일 */
    .css-163u3g {
        background-color: #1E1E1E;
    }
    
    /* 사이드바 텍스트 색상 */
    .css-1v3fvcr {
        color: white;
    }
    
    /* 제목 스타일 */
    h1, h2, h3 {
        color: white !important;
    }
    
    /* 사이드바 내부 설정 제목 */
    .sidebar-header {
        font-size: 20px;
        font-weight: bold;
        margin-top: 10px;
        color: #A0A0A0;
    }
    
    /* 사이드바 번호 매기기 */
    .sidebar-number {
        font-weight: bold;
        margin-right: 5px;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        border-radius: 0px; /* 네모 */
        border: none;
        padding: 0;
        transition: background-color 0.3s ease;
        height: 25vh; /* 화면 높이의 25% */
        width: 100%;
        color: white;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* 블록 아이콘 스타일 */
    .block-icon {
        font-size: 60px;
        margin-bottom: 15px;
        color: white;
    }
    
    /* 블록 텍스트 스타일 */
    .block-title {
        font-size: 22px;
        font-weight: bold;
        color: white;
    }
    
    /* 각 블록의 배경색 */
    .red-block {
        background-color: #E74C3C; /* image_1.png의 빨간색 */
    }
    
    .green-block {
        background-color: #2ECC71; /* image_1.png의 초록색 */
    }
    
    .blue-block {
        background-color: #3498DB; /* image_1.png의 파란색 */
    }
    
    /* 오디오 플레이어 스타일 숨기기 (깔끔하게) */
    audio { width: 100%; margin-top: 10px; }
    
</style>
""", unsafe_allow_html=True)

# 💡 리셋 카운터 초기화
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

def reset_all():
    st.session_state.reset_key += 1
    # 세션에 저장된 커스텀 컬러 등도 삭제
    for key in list(st.session_state.keys()):
        if key != "reset_key":
            del st.session_state[key]

# 고유 접미사 (리셋될 때마다 바뀜)
suffix = f"_{st.session_state.reset_key}"

st.markdown("<h2 style='text-align: center; margin-top: 0px;'>🎙️ 리버스 보이스 플레이어</h2>", unsafe_allow_html=True)

# --- 사이드바 ---
st.sidebar.markdown("<div class='sidebar-header'>🛠️ 앱 설정</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<span class='sidebar-number'>1️⃣</span> 화면 비율 설정", unsafe_allow_html=True)
    cat = st.selectbox("기기 분류", ["스마트폰 (1080x2340)", "태블릿 (2048x2732)", "이북 리더기 (758x1024)", "직접 입력"], index=2, key=f"cat{suffix}")
    res = {"스마트폰 (1080x2340)": (1080, 2340), "태블릿 (2048x2732)": (2048, 2732), "이북 리더기 (758x1024)": (758, 1024)}
    
    if cat == "직접 입력":
        w = st.number_input("가로", value=1080, key=f"w{suffix}")
        h = st.number_input("세로", value=1920, key=f"h{suffix}")
    else:
        w, h = res[cat]
    
    st.markdown("---")
    st.markdown("<span class='sidebar-number'>2️⃣</span> 달력 시기 및 위치", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    year = c1.number_input("년", value=2026, key=f"year{suffix}")
    month = c2.number_input("월", 1, 12, 3, key=f"month{suffix}")
    is_landscape = st.checkbox("🔄 가로로 돌리기", value=False, key=f"land{suffix}")
    if is_landscape: w, h = h, w
    use_holidays = st.checkbox("대한민국 공휴일 반영", value=True, key=f"hol{suffix}")
    pos_val = st.slider("세로 위치 (%)", 0, 100, 50, key=f"pos{suffix}")
    
    st.markdown("---")
    st.markdown("<span class='sidebar-number'>3️⃣</span> 배경 설정", unsafe_allow_html=True)
    bg_type = st.radio("배경 종류", ["단색 컬러", "이미지 업로드"], horizontal=True, key=f"bg_t{suffix}")
    
    bg_rotate, bg_x, bg_y, bg_zoom, bg_img, bg_color = 0, 0, 0, 1.0, None, "#FFFFFF"
    
    if bg_type == "이미지 업로드":
        bg_img = st.file_uploader("이미지 파일 선택", type=['jpg', 'png', 'jpeg'], key=f"bg_img{suffix}")
        st.write("🖼️ **이미지 조작**")
        bg_rotate = st.slider("이미지 회전 (도)", 0, 360, 0, 1, key=f"bg_r{suffix}")
        bg_zoom = st.slider("이미지 확대 (Zoom)", 1.0, 3.0, 1.0, 0.1, key=f"bg_z{suffix}")
        bg_x = st.slider("이미지 가로 이동 (%)", -100, 100, 0, key=f"bg_x{suffix}")
        bg_y = st.slider("이미지 세로 이동 (%)", -100, 100, 0, key=f"bg_y{suffix}")
        bg_color = st.color_picker("이미지 외곽 배경색", "#FFFFFF", key=f"bg_c_img{suffix}")
    else:
        bg_color = st.color_picker("배경색 선택", "#FFFFFF", key=f"bg_c_plain{suffix}")
    
    show_box = st.checkbox("가독성 박스 추가(이미지 배경 시)", value=False, key=f"s_box{suffix}")
    if show_box:
        bx_c = st.color_picker("바탕 박스 색상", "#FFFFFF", key=f"bx_c{suffix}")
        bx_o = st.slider("바탕 투명도", 0, 100, 75, key=f"bx_o{suffix}")
        bx_r = st.slider("바탕 모서리 곡률", 0, 100, 20, key=f"bx_r{suffix}")
    else: bx_c, bx_o, bx_r = "#FFFFFF", 75, 20
    
    st.markdown("---")
    st.markdown("<span class='sidebar-number'>4️⃣</span> 텍스트 설정", unsafe_allow_html=True)
    lang = st.radio("언어", ["English", "한국어"], horizontal=True, key=f"lang{suffix}")
    font_f = st.selectbox("서체", ["Arial", "맑은 고딕", "바탕체", "나눔고딕"], index=0, key=f"font{suffix}")
    is_bold = st.checkbox("볼드체 설정", value=False, key=f"bold{suffix}")
    with st.expander("외부 폰트 추가"):
        up_font = st.file_uploader("폰트 파일 (.ttf, .otf)", type=['ttf', 'otf'], key=f"up_f{suffix}")
    
    t_color = st.color_picker("텍스트 색상", "#000000", key=f"t_c{suffix}")
    f_size = st.slider("글자 크기", 10, 120, 30, key=f"f_s{suffix}")
    with st.expander("📏 간격 세부 설정"):
        x_s = st.slider("가로 간격", 1.0, 5.0, 2.5, key=f"x_s{suffix}")
        y_s = st.slider("세로 간격", 1.0, 5.0, 2.0, key=f"y_s{suffix}")
    
    st.markdown("---")
    st.markdown("<span class='sidebar-number'>5️⃣</span> 출처 텍스트 표기", unsafe_allow_html=True)
    show_moon1 = st.checkbox("제작자 표시 (Moon1)", value=False, key=f"s_m1{suffix}")
    show_custom = st.checkbox("싫어요 내 이름 적을꺼야", value=False, key=f"s_c{suffix}")
    custom_text = ""
    if show_custom:
        custom_text = st.text_input("적고 싶은 문구 입력", value="내 이름", key=f"c_txt{suffix}")
    wm_color = st.color_picker("하단 글자 색상", "#000000", key=f"wm_c{suffix}")
    
    st.markdown("---")
    st.markdown("<span class='sidebar-number'>6️⃣</span> 초기화", unsafe_allow_html=True)
    # 💡 새로운 리셋 함수 호출
    if st.button("모두 기본값으로", key="reset_btn"):
        reset_all()
        st.rerun()

    st.caption("🚀 최종 수정: 2026.03.15.04.40")

# --- 메인 영역 ---

# 오디오 상태 관리💡
if 'audio_processed' not in st.session_state:
    st.session_state.audio_processed = None
if 'play_recorded' not in st.session_state:
    st.session_state.play_recorded = False
if 'play_reverse' not in st.session_state:
    st.session_state.play_reverse = False

# --- 1. 녹음 섹션 (Red Block) ---
# 💡 mic_recorder 위젯은 커스텀 CSS 클래스를 직접 지원하지 않으므로, 이미지 1의 빨간색을 적용하고 테두리 곡률을 0으로 만들어 모방합니다.
audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="🛑 Stop Recording",
    key='recorder',
    css=f"border-radius: 0; background-color: #E74C3C; height: 25vh; width: 100%; border: none; transition: background-color 0.3s ease; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 24px; color: white;"
)

# --- 오디오 처리 로직 (V19) ---
if audio:
    audio_bytes = audio['bytes']
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
    
    # 역방향 처리💡
    reversed_audio = audio_segment.reverse()
    buf = io.BytesIO()
    reversed_audio.export(buf, format="wav")
    st.session_state.audio_processed = buf.getvalue()
    
    # 2. 정방향 재생 섹션 (Green Block)💡
    st.markdown("---")
    # 💡 커스텀 CSS 클래스 적용
    st.markdown(f"""
    <div class='stButton'>
        <button class='block-content green-block' key="play_recorded_btn" onclick="Streamlit.setComponentValue('play_recorded', true)">
            <div class='block-icon'>▶️</div>
            <div class='block-title'>Play Recorded</div>
        </button>
    </div>
    """, unsafe_allow_html=True)
    # 오디오 재생을 위한 숨겨진 위젯💡
    if st.session_state.play_recorded:
        st.audio(audio_bytes)
        st.session_state.play_recorded = False # 재생 후 상태 초기화

    # 3. 역방향 처리 섹션 (Blue Block)💡
    st.markdown("---")
    # 💡 커스텀 CSS 클래스 적용
    st.markdown(f"""
    <div class='stButton'>
        <button class='block-content blue-block' key="play_reverse_btn" onclick="Streamlit.setComponentValue('play_reverse', true)">
            <div class='block-icon'>⏪</div>
            <div class='block-title'>Play Reverse</div>
        </button>
    </div>
    """, unsafe_allow_html=True)
    # 오디오 재생을 위한 숨겨진 위젯💡
    if st.session_state.play_reverse and st.session_state.audio_processed is not None:
        st.audio(st.session_state.audio_processed)
        st.session_state.play_reverse = False # 재생 후 상태 초기화
    
    st.success("✨ 목소리를 성공적으로 뒤집었습니다! 신기하죠?")

else:
    st.info("💡 빨간색 버튼 영역에서 '녹음 시작하기'를 눌러보세요.")
    
# 재생 완료 알림 (브라우저 정책에 따라 불가능할 수 있음)💡
# st.markdown(f"<script>Streamlit.setComponentValue('audio_processed', null)</script>", unsafe_allow_html=True)
