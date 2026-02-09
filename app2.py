import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered", page_title="ことばの訓練")

# 2. デザインの調整 (CSS)
st.markdown("""
    <style>
   /* アプリ全体（根っこ）を強制的に白くする */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stApp {
        background-color: #FFFFFF !important;
    }
    }
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    /* タイトルの文字 */
    .title-text {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* 正解文字のデザイン（色を黒に修正） */
    .answer-text {
        text-align: center;
        font-size: 80px;
        font-weight: bold;
        color: #000000; /* ★ここを黒に変更しました */
        margin: 20px 0;
    }
    /* 画像を中央に固定する設定 */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto !important;
        margin-right: auto !important;
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
course_animals2 = [
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
# ■ メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    # ★ 2個から3個に変更し、col3を追加します
    col1, col2, col3 = st.columns(3)
    
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

    # ★ col3の設定を追加
    with col3:
        if st.button("🦁 動物カテゴリー2"):
            # ここは course_animals2 を使うように修正しました
            st.session_state.card_list = course_animals2.copy()
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

    # 終了判定
    if idx >= len(cards):
        st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        st.markdown(f"<p style='text-align: center;'>第 {idx + 1} 問 / {len(cards)} 問</p>", unsafe_allow_html=True)

        # 画像の表示
        if not st.session_state.show_answer:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if os.path.exists(target['filename']):
                    st.image(target['filename'], use_container_width=True)
                else:
                    st.error(f"画像が見つかりません: {target['filename']}")
            
            # 答えを見るボタン
            st.write("")
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

        # 正解の表示
        else:
            st.markdown(f"<div class='answer-text'>{target['answer']}</div>", unsafe_allow_html=True)
            
            n1, n2, n3 = st.columns([1, 2, 1])
            with n2:
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
