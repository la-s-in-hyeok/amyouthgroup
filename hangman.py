import streamlit as st
import random
import re

# 찬양 리스트
songs = [
    "나로부터 시작되리", "하나님의 사랑이", "주의 나라가 비전인 세대", "우리 주 안에서 노래하며",
    "유월절 어린 양의 피로", "예수 열방의 소망", "우리 죄 위해 죽으신 주", "여호와께 돌아가자",
    "주님만이 왕이십니다", "예수 나의 첫사랑 되시네", "내 마음을 가득채운", "하나님께서 세상을 사랑하사",
    "내 영혼은 안전합니다", "성령의 불타는 교회", "성령이 오셨네", "주님 다시 오실 때까지",
    "온 세상 창조주", "부르신 곳에서", "주님 다시 오실 때까지", "주 사랑이 내게 들어와", "나를 향한 주의 사랑","지극히 높으신 주", "모든 생명들아 소리쳐",
    "태산을 넘어 험곡에 가도", "그가 다스리는 그의 나라에서", "우린 물러서지 않으리", "어둠을 찢으신 빛", "어둔 날 다 지나고"
]

# 세션 상태 초기화
def init_game():
    st.session_state['selected_song'] = random.choice(songs)
    st.session_state['display_word'] = re.sub(r'[^ ]', '_', st.session_state['selected_song'])
    st.session_state['remaining_attempts'] = 12
    st.session_state['guessed_letters'] = set()
    st.session_state['guessed_words'] = []
    st.session_state['game_over'] = False
    st.session_state['message'] = ""

if 'selected_song' not in st.session_state:
    init_game()

st.title("공동체 훈련[찬양] 6번, 행맨 게임")
st.subheader("제목을 맞춰보세요!")

# 현재 상태 표시
st.write("현재 상태(업데이트 되는게 느려요 이해좀): ", st.session_state['display_word'])
st.write(f"남은 기회: {st.session_state['remaining_attempts']}")

if not st.session_state['game_over']:
    col1, col2 = st.columns(2)
    with col1:
        user_input = st.text_input("한 글자를 입력하세요:", max_chars=1, key="user_input")
        submit_letter = st.button("글자 제출(더블 클릭)")
    with col2:
        full_guess = st.text_input("정답을 입력하세요:", key="full_guess")
        submit_word = st.button("정답 제출(더블 클릭)")
    
    if submit_letter and user_input:
        user_input = user_input.strip()
        if user_input in st.session_state['guessed_letters']:
            st.session_state['message'] = "이미 입력한 글자입니다!"
        else:
            st.session_state['guessed_letters'].add(user_input)
            
            if user_input in st.session_state['selected_song']:
                st.session_state['message'] = "정답입니다!"
            else:
                st.session_state['message'] = "틀렸습니다!"
                st.session_state['remaining_attempts'] -= 1
            
            # 언더바 업데이트
            st.session_state['display_word'] = "".join(
                c if c in st.session_state['guessed_letters'] or c == " " else "_"
                for c in st.session_state['selected_song']
            )
            
            # 정답 확인
            if "_" not in st.session_state['display_word']:
                st.session_state['game_over'] = True
                st.success(f"축하합니다! God bless you!! 정답: {st.session_state['selected_song']}")
                st.markdown("<h1 style='font-size:100px; text-align:center;'>1</h1>", unsafe_allow_html=True)
    
    if submit_word and full_guess:
        full_guess = full_guess.strip()
        st.session_state['guessed_words'].append(full_guess)
        
        if full_guess == st.session_state['selected_song']:
            st.session_state['game_over'] = True
            st.success(f"축하합니다! 은혜 많이 받으세요! 정답: {st.session_state['selected_song']}")
            st.markdown("<h1 style='font-size:100px; text-align:center;'>1</h1>", unsafe_allow_html=True)
        else:
            st.session_state['message'] = "틀렸습니다! 다시 시도하세요."
            st.session_state['remaining_attempts'] -= 1
    
    # 남은 기회가 0이어도 정답을 다 맞혔다면 게임 오버 처리 X
    if st.session_state['remaining_attempts'] <= 0 and "_" in st.session_state['display_word']:
        st.session_state['game_over'] = True
        st.error(f"게임 오버! 정답은 '{st.session_state['selected_song']}'였습니다.")
    
    # 메시지 출력
    st.write(f"### {st.session_state['message']}")
    
    # 입력한 글자 및 정답 히스토리 표시
    st.write("### 입력한 글자들: ", ", ".join(sorted(st.session_state['guessed_letters'])))
    st.write("### 입력한 정답들: ", ", ".join(st.session_state['guessed_words']))
else:
    if st.button("다시 시작하기"):
        init_game()
