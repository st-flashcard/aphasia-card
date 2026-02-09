import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# CSS設定（ここを強力にしました！）
st.markdown("""
    <style>
    /* 全体の余白調整 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* ★魔法の呪文1：画像を強制的に真ん中に配置 */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center;
        align-items: center;
    }

    /* ★魔法の呪文2：ボタンを強制的に真ん中に配置 */
    .stButton {
        display: flex;
        justify_content: center;
    }
    
    /* ボタン自体のデザイン */
    .stButton button {
        width: 100%;         /* 基本は横幅いっぱい */
        max-width: 300px;    /* ただし300px以上は大きくならない（スマホで見やすい） */
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* ちょっと影をつける */
    }

    /* タイトル文字 */
    .title-text {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* 第○問の文字 */
    .question-text {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #555;
        margin-bottom: 10px;
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

# ■ パターン1：メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    # メニューボタンも真ん中に寄せるために columns は使わずそのまま表示
    # (CSSで真ん中になるように設定してあります)
    
    st.write("")
    if st.button("🍎 基本の単語"):
        st.session_state.card_list = course_basic.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun
