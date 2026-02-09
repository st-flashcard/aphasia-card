import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered") # これで最初からある程度真ん中に寄ります

# 2. デザイン調整（ボタンの見た目だけ整えます。配置はいじりません）
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        height: 60px;
        margin-top: 10px;
        margin-bottom: 10px;
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

# ----------------------------------------
# 画面の表示
# ----------------------------------------

# ■ パターン1：メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>訓練メニューを選んでください</h2>", unsafe_allow_html=True)
    
    # 画面を「左・中・右」に分けます（比率は 1 : 2 : 1）
    # 真ん中（col2）にだけボタンを置きます
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
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

# ■ パターン2：ゲーム画面
elif st.session_state.mode == 'game':
    
    # サイドバー（メニュー）
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

    # データチェック
    if not st.session_state.card_list:
        st.error("エラー：データがありません")
        if st.button("戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        idx = st.session_state.current_index
        cards = st.session_state.card_list

        # 終了画面
        if idx >= len(cards):
            st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("メニューに戻る"):
                    st.session_state.mode = 'menu'
                    st.rerun()

        # 問題表示画面
        else:
            target = cards[idx]

            # 1. 第○問（文字を真ん中に）
            st.markdown(f"<h3 style='text-align: center;'>第 {idx + 1} 問</h3>", unsafe_allow_html=True)
            st.write("") # 少し隙間

            # 2. 画像とボタン（ここも「左・中・右」作戦！）
            col1, col2, col3 = st.columns([1, 4, 1])
