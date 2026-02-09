import streamlit as st
import random
import os

# 1. ページ設定
st.set_page_config(layout="centered")

# 2. デザインの微調整（余白を削ってスクロールを防止）
st.markdown("""
    <style>
    /* 画面一番上の余白を最小限にする */
    .block-container {
        padding-top: 10px !important;
        padding-bottom: 0px !important;
    }
    /* ボタンの文字を大きく、高さは控えめに */
    .stButton button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }
    /* 文字の隙間を詰める */
    p, h3, h2 {
        margin: 0px !important;
        padding: 5px !important;
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
    {"filename": "panda.jpg",    "answer": "ぱんだ"},
    {"filename": "lion.jpg",     "answer": "らいおん"},
    {"filename": "elephant.jpg", "answer": "ぞう"},
    {"filename": "penguin.jpg",  "answer": "ぺんぎん"},
]

# 4. 状態管理
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# --- 画面表示 ---

# ■ メニュー画面
if st.session_state.mode == 'menu':
    st.write("### コースを選んでください")
    
    # [1, 2, 1]の比率で列を作り、真ん中にボタンを配置
    c1, col2, c3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🍎 基本の単語"):
            st.session_state.card_list = course_basic.copy()
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = 'game'
            st.rerun()
        
        st.write("") # 隙間
        
        if st.button("🐶 動物カテゴリー"):
            st.session_state.card_list = course_animals.copy()
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = 'game'
            st.rerun()

# ■ ゲーム画面
elif st.session_state.mode == 'game':
    idx = st.session_state.current_index
    cards = st.session_state.card_list

    if idx >= len(cards):
        st.write("## 🎉 お疲れ様でした！")
        c1, col2, c3 = st.columns([1, 2, 1])
        with col2:
            if st.button("メニューへ戻る"):
                st.session_state.mode = 'menu'
                st.rerun()
    else:
        target = cards[idx]
        st.write(f"第 {idx + 1} 問")

        # 画面を [1, 2, 1] に分割して中央寄せ
        c1, col2, c3 = st.columns([1, 2, 1])
        
        with col2:
            if not st.session_state.show_answer:
                # ★画像を「幅200px」に。これでボタンが必ず見えます！
                if os.path.exists(target['filename']):
                    st.image(target['filename'], width=200)
                else:
                    st.error("画像なし")
                
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                # 正解を表示
                st.write(f"## {target['answer']}")
                st.write("")
                if st.button("次の問題へ"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()

        # 画面一番下にこっそり戻るボタン
        st.write("---")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("やめる", key="exit"):
                st.session_state.mode = 'menu'
                st.rerun()
