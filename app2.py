import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# CSS設定
st.markdown("""
    <style>
    /* ボタンのデザイン */
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    /* タイトルのデザイン */
    .title-text {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* 正解文字のスタイル */
    .answer-text {
        text-align: center;
        font-size: 80px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #FF4B4B; /* 少し色をつけて目立たせました */
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 1. データの準備
# ----------------------------------------
course_basic = [
    {"filename": "apple.jpg", "answer": "りんご"},
    {"filename": "cat.jpg",   "answer": "ねこ"},
    {"filename": "pen.jpg",   "answer": "ぺん"},
    {"filename": "watch.jpg", "answer": "とけい"},
    {"filename": "book.jpg",  "answer": "ほん"},
]

course_animals = [
    {"filename": "dog.jpg",      "answer": "いぬ"},
    {"filename": "cat.jpg",      "answer": "ねこ"},
    {"filename": "panda.jpg",    "answer": "ぱんだ"},
    {"filename": "lion.jpg",     "answer": "らいおん"},
    {"filename": "giraffe.jpg",  "answer": "きりん"},
    {"filename": "elephant.jpg", "answer": "ぞう"},
    {"filename": "koala.jpg",    "answer": "こあら"},
    {"filename": "gorilla.jpg",  "answer": "ごりら"},
    {"filename": "penguin.jpg",  "answer": "ぺんぎん"},
    {"filename": "tiger.jpg",    "answer": "とら"},
]

# ----------------------------------------
# 2. アプリの状態管理
# ----------------------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ----------------------------------------
# 3. 画面の表示
# ----------------------------------------

if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍎 基本の単語"):
            st.session_state.card_list = course_basic.copy()
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = 'game'
            st.rerun()
    with col2:
        if st.button("🐶 動物カテゴリー"):
            st.session_state.card_list = course_animals.copy()
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = 'game'
            st.rerun()

elif st.session_state.mode == 'game':
    with st.sidebar:
        st.write("メニュー")
        if st.button("← メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
        if st.button("もう一度シャッフル"):
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

    if not st.session_state.card_list:
        st.error("データがありません。メニューに戻ってください。")
    else:
        idx = st.session_state.current_index
        cards = st.session_state.card_list

        if idx >= len(cards):
            st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
            if st.button("メニューに戻る"):
                st.session_state.mode = 'menu'
                st.rerun()
        else:
            target = cards[idx]
            st.markdown(f"<div style='text-align: center; font-size: 18px; margin-bottom: 10px;'>第 {idx + 1} 問</div>", unsafe_allow_html=True)

            # --- ここから画像表示の修正 ---
            if not st.session_state.show_answer:
                # 3つのカラムを作り、真ん中（col2）を広くします。
                # [1, 2, 1] の比率で、真ん中の 2 が画像エリアになります。
                col1, col2, col3 = st.columns([0.5, 2, 0.5]) 
                
                with col2:
                    if os.path.exists(target['filename']):
                        # use_container_width=True にすることで、
                        # 「真ん中のカラムの横幅いっぱい」に画像が表示されます。
                        st.image(target['filename'], use_container_width=True)
                    else:
                        st.error(f"画像が見つかりません: {target['filename']}")
                
                # 答えを見るボタン
                st.write("") 
                bc1, bc2, bc3 = st.columns([1, 2, 1]) 
                with bc2:
                    if st.button("答えを見る"):
                        st.session_state.
