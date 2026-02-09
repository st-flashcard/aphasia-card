import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered")

# 2. デザイン調整（高さを抑えるための最小限のCSS）
st.markdown("""
    <style>
    /* 画面上部の余白をギリギリまで削る */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    /* ボタンのサイズを少しコンパクトに */
    .stButton button {
        width: 100%;
        max-width: 250px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }
    /* テキストの余白を詰める */
    p, h1, h2, h3 {
        margin-top: 0px !important;
        margin-bottom: 5px !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. データの準備
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

# 4. アプリの状態管理
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# --- 画面表示 ---

if st.session_state.mode == 'menu':
    st.write("### 訓練メニュー")
    
    # メニュー画面もコンパクトに配置
    if st.button("🍎 基本の単語コース"):
        st.session_state.card_list = course_basic.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun()

    if st.button("🐶 動物カテゴリーコース"):
        st.session_state.card_list = course_animals.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun()

elif st.session_state.mode == 'game':
    
    with st.sidebar:
        if st.button("← メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()

    idx = st.session_state.current_index
    cards = st.session_state.card_list

    if idx >= len(cards):
        st.write("## 🎉 おつかれさまでした！")
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        st.write(f"第 {idx + 1} 問")

        # --- ここがポイント：スクロールを防ぐ配置 ---
        
        # 1. 答えを見る前
        if not st.session_state.show_answer:
            if os.path.exists(target['filename']):
                # ★画像を幅250pxに制限して、高さを抑えます
                st.image(target['filename'], width=250)
            else:
                st.error("画像なし")
            
            # 中央寄せにするために空の列で挟む
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

        # 2. 答えを見た後
        else:
            # 正解の文字を少し控えめなサイズ（h2）に
            st.write(f"## {target['answer']}")
            
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if st.button("次の問題へ"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
