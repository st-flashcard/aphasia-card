import streamlit as st
import random
import os

# 1. ページの設定（centeredにすると全体が中央に寄ります）
st.set_page_config(layout="centered")

# 2. デザインの微調整（ボタンの高さだけを抑えます）
st.markdown("""
    <style>
    /* 画面上の余白を消す */
    .block-container {
        padding-top: 1rem !important;
    }
    /* ボタンを少し低くしてスペースを節約 */
    .stButton button {
        height: 45px;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. データの準備（動物リスト）
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

# --- 画面の表示 ---

# ■ メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("<h3 style='text-align: center;'>コースを選択</h3>", unsafe_allow_html=True)
    
    # [1, 2, 1] の比率で列を作り、真ん中（col2）にだけボタンを置いて中央寄せにします
    c1, col2, c3 = st.columns([1, 2, 1])
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

# ■ ゲーム画面（訓練中）
elif st.session_state.mode == 'game':
    idx = st.session_state.current_index
    cards = st.session_state.card_list

    # 終了判定
    if idx >= len(cards):
        st.markdown("<h3 style='text-align: center;'>🎉 お疲れ様でした！</h3>", unsafe_allow_html=True)
        c1, col2, c3 = st.columns([1, 1, 1])
        with col2:
            if st.button("メニューへ"):
                st.session_state.mode = 'menu'
                st.rerun()
    else:
        target = cards[idx]
        
        # 1. 第○問（中央寄せ）
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>第 {idx + 1} 問</p>", unsafe_allow_html=True)

        # 2. メインエリア（列を使って中央寄せ）
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not st.session_state.show_answer:
                # ★画像を「width=150」に。これで確実にボタンが画面内に収まります！
                if os.path.exists(target['filename']):
                    st.image(target['filename'], width=150)
                else:
                    st.error("画像なし")
                
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                # 答えの文字
                st.markdown(f"<h2 style='text-align: center;'>{target['answer']}</h2>", unsafe_allow_html=True)
                if st.button("次へ進む"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()

    # 下の方に「メニューに戻る」を配置
    st.divider()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("← 戻る", key="back_btn"):
            st.session_state.mode = 'menu'
            st.rerun()
