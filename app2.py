import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered", page_title="ことばの訓練")

# 2. デザインの調整 (CSS)
st.markdown("""
    <style>
    /* ボタンを中央に寄せて、見やすくする */
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton button {
        width: 100%; /* カラム幅いっぱいに広げる */
        max-width: 300px; /* 広がりすぎないように制限 */
        height: 60px;
        font-size: 22px;
        font-weight: bold;
    }
    /* タイトルの文字 */
    .title-text {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* 正解文字のデザイン（色は黒） */
    .answer-text {
        text-align: center;
        font-size: 80px;
        font-weight: bold;
        color: #000000;
        margin: 20px 0;
    }
    /* 画像を中央に固定する設定 */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto !important;
        margin-right: auto !important;
        border: 1px solid #ddd; /* 輪郭を少し見やすく */
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 3. データの準備
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
# 4. アプリの状態管理
# ----------------------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ----------------------------------------
# 5. 画面表示のロジック
# ----------------------------------------

# ■ メニュー画面
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

# ■ ゲーム画面
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
        # 終了画面のボタンも中央寄せ
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        st.markdown(f"<p style='text-align: center;'>第 {idx + 1} 問 / {len(cards)} 問</p>", unsafe_allow_html=True)

        # 画像の表示
        if not st.session_state.show_answer:
            # 枠を中央に配置
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            with c2:
                if os.path.exists(target['filename']):
                    st.image(target['filename'], use_container_width=True)
                else:
                    st.error(f"画像が見つかりません: {target['filename']}")
            
            # 答えを見るボタン (こちらも中央カラムに配置)
            st.write("")
            with c2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

        # 正解の表示
        else:
            st.markdown(f"<div class='answer-text'>{target['answer']}</div>", unsafe_allow_html=True)
            
            # 次の問題へボタン (中央に配置)
            _, n_col, _ = st.columns([0.5, 2, 0.5])
            with n_col:
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
