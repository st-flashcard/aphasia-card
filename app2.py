import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered")

# 2. 強力なデザイン調整（余白を極限までカット）
st.markdown("""
    <style>
    /* 画面上部の大きな余白を消す */
    .block-container {
        padding-top: 10px !important;
        padding-bottom: 0px !important;
        max-width: 500px !important;
    }
    /* 画像の上下の無駄な隙間を消す */
    [data-testid="stImage"] {
        margin-top: -20px !important;
        margin-bottom: -10px !important;
        display: flex;
        justify-content: center;
    }
    /* ボタンを押しやすく、かつ高さを抑える */
    .stButton button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    /* 全ての文字を真ん中寄せに */
    h1, h2, h3, p, div {
        text-align: center !important;
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
    {"filename": "panda.jpg",    "answer": "ぱんだ"},
    {"filename": "lion.jpg",     "answer": "らいおん"},
    {"filename": "elephant.jpg", "answer": "ぞう"},
    {"filename": "penguin.jpg",  "answer": "ぺんぎん"},
]

# 4. アプリの状態管理
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ----------------------------------------
# 3. 画面の表示
# ----------------------------------------

# ■ メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("### 訓練メニュー")
    
    if st.button("🍎 基本の単語"):
        st.session_state.card_list = course_basic.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun()

    if st.button("🐶 動物カテゴリー"):
        st.session_state.card_list = course_animals.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun()

# ■ ゲーム画面
elif st.session_state.mode == 'game':
    
    # 画面上部に戻るボタンを設置（サイドバーは場所をとるので使いません）
    if st.button("← メニューに戻る", key="back"):
        st.session_state.mode = 'menu'
        st.rerun()

    idx = st.session_state.current_index
    cards = st.session_state.card_list

    if idx >= len(cards):
        st.markdown("## 🎉 おつかれさま！")
        if st.button("メニューへ戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]

        # 1. 何問目か（小さく表示）
        st.write(f"第 {idx + 1} 問")

        # 2. 画像（高さを抑えるために width=200 程度に制限）
        if not st.session_state.show_answer:
            if os.path.exists(target['filename']):
                st.image(target['filename'], width=220)
            else:
                st.error("画像なし")
            
            # 3. 答えボタン
            if st.button("答えを見る"):
                st.session_state.show_answer = True
                st.rerun()

        # 4. 答えを表示
        else:
            # 文字が大きすぎるとボタンが下に行くのでサイズを調整
            st.markdown(f"<h1 style='font-size: 60px;'>{target['answer']}</h1>", unsafe_allow_html=True)
            
            if st.button("次の問題へ", type="primary"):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
