import streamlit as st
import random
import os

# 1. ページの設定（これだけで基本は十分です）
st.set_page_config(layout="centered")

# 2. データの準備（動物リストも入っています）
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

# 3. アプリの状態管理
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# --- 画面表示 ---

# ■ パターン1：メニュー画面
if st.session_state.mode == 'menu':
    st.write("### 訓練メニューを選んでください") # タイトルを表示
    
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

# ■ パターン2：ゲーム画面（訓練中）
elif st.session_state.mode == 'game':
    
    # 左側のメニューに戻るボタン
    with st.sidebar:
        if st.button("← メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()

    idx = st.session_state.current_index
    cards = st.session_state.card_list

    # 終了判定
    if idx >= len(cards):
        st.write("## 🎉 おつかれさまでした！")
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        st.write(f"第 {idx + 1} 問") # 何問目か表示

        # 答えを見る前
        if not st.session_state.show_answer:
            # 画像があるかチェック
            if os.path.exists(target['filename']):
                st.image(target['filename'], use_container_width=True)
            else:
                st.error(f"画像ファイルが見つかりません: {target['filename']}")
            
            # 答えボタン
            if st.button("答えを見る"):
                st.session_state.show_answer = True
                st.rerun()

        # 答えを見た後
        else:
            st.write(f"# {target['answer']}") # 大きく答えを表示
            
            if st.button("次の問題へ"):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
