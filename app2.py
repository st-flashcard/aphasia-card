import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered", page_title="ことばの訓練")

# 2. デザインの調整
st.markdown("""
    <style>
    .stButton button { width: 100%; height: 60px; font-size: 18px; font-weight: bold; }
    .title-text { text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .answer-text { text-align: center; font-size: 80px; font-weight: bold; color: #000000; margin: 20px 0; }
    [data-testid="stImage"] img { display: block; margin-left: auto !important; margin-right: auto !important; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 3. データの準備（名前を短くしました！）
# ----------------------------------------
course_basic = [
    {"filename": "apple.jpg", "answer": "りんご"},
    {"filename": "cat.jpg",   "answer": "ねこ"},
    {"filename": "pen.jpg",   "answer": "ぺん"},
    {"filename": "watch.jpg", "answer": "とけい"},
    {"filename": "book.jpg",  "answer": "ほん"},
]

course_animals_1 = [
    {"filename": "dog.jpg",      "answer": "いぬ"},
    {"filename": "cat.jpg",      "answer": "ねこ"},
    {"filename": "panda.jpg",    "answer": "ぱんだ"},
    {"filename": "lion.jpg",     "answer": "らいおん"},
    {"filename": "penguin.jpg",  "answer": "ぺんぎん"},
]

course_animals_2 = [
    {"filename": "bear.jpg",     "answer": "くま"},
    {"filename": "owl.jpg",      "answer": "ふくろう"},
    {"filename": "deer.jpg",     "answer": "しか"},
    {"filename": "zebra.jpg",    "answer": "しまうま"},
    {"filename": "kangaroo.jpg", "answer": "かんがるー"},
    {"filename": "rabbit.jpg",   "answer": "うさぎ"},
    {"filename": "monkey.jpg",   "answer": "さる"},
    {"filename": "squirrel.jpg", "answer": "りす"},
    {"filename": "sheep.jpg",    "answer": "ひつじ"},
    {"filename": "pig.jpg",      "answer": "ぶた"},
]

# ----------------------------------------
# 4. 状態管理
# ----------------------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ----------------------------------------
# 5. 画面表示
# ----------------------------------------

if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍎 基本"):
            st.session_state.card_list = course_basic.copy()
            st.session_state.mode = 'game'
            
    with col2:
        if st.button("🐶 動物 1"):
            st.session_state.card_list = course_animals_1.copy()
            st.session_state.mode = 'game'

    with col3:
        if st.button("🐨 動物 2"):
            st.session_state.card_list = course_animals_2.copy()
            st.session_state.mode = 'game'
    
    # コース選択後の共通処理
    if st.session_state.mode == 'game':
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.rerun()

elif st.session_state.mode == 'game':
    with st.sidebar:
        if st.button("← メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
        if st.button("もう一度シャッフル"):
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

    idx = st.session_state.current_index
    cards = st.session_state.card_list

    if idx >= len(cards):
        st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        st.markdown(f"<p style='text-align: center;'>第 {idx + 1} 問 / {len(cards)} 問</p>", unsafe_allow_html=True)

        if not st.session_state.show_answer:
            if os.path.exists(target['filename']):
                st.image(target['filename'], width=250)
            else:
                st.error(f"画像が見つかりません: {target['filename']}")
            
            st.write("")
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()
        else:
            st.markdown(f"<div class='answer-text'>{target['answer']}</div>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1, 2, 1])
            with n2:
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
