import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered")

# 2. デザイン調整（高さを最小限にするためのCSS）
st.markdown("""
    <style>
    /* 1. 画面上部の余白を完全にゼロにする */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
    }
    /* 2. 画像の上下の隙間を消す */
    [data-testid="stImage"] {
        margin-top: -10px !important;
        margin-bottom: -10px !important;
    }
    /* 3. ボタンを少し小さく、余白も詰める */
    .stButton button {
        width: 100%;
        max-width: 200px;
        height: 45px;
        font-size: 16px;
        margin-top: 0px !important;
    }
    /* 4. 文字サイズを小さくして一行に収める */
    h3, h2, h1, p {
        margin: 0px !important;
        padding: 0px !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. データの準備（中身はそのまま）
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

# 4. 状態管理
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# --- 画面表示 ---

if st.session_state.mode == 'menu':
    st.markdown("### 訓練メニュー")
    if st.button("🍎 基本"):
        st.session_state.card_list = course_basic.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun()
    if st.button("🐶 動物"):
        st.session_state.card_list = course_animals.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun()

elif st.session_state.mode == 'game':
    # サイドバーは閉じている前提で進めます
    with st.sidebar:
        if st.button("← 戻る"):
            st.session_state.mode = 'menu'
            st.rerun()

    idx = st.session_state.current_index
    cards = st.session_state.card_list

    if idx >= len(cards):
        st.write("## 🎉 お疲れ様！")
        if st.button("メニューへ"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        
        # 1. 第○問（小さく表示）
        st.markdown(f"**第 {idx + 1} 問**")

        # 2. 画像（思い切ってさらに小さく width=180）
        if os.path.exists(target['filename']):
            # ★ここをさらに小さくしました！
            st.image(target['filename'], width=180)
        
        # 3. ボタンと正解表示
        if not st.session_state.show_answer:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()
        else:
            # 答えの文字サイズを調整（大きすぎないように）
            st.markdown(f"## {target['answer']}")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("次へ"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
