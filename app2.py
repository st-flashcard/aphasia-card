import streamlit as st
import random
import os

# 1. ページの設定（レイアウトを「centered」にするだけで、基本は真ん中に寄ります）
st.set_page_config(layout="centered")

# 2. デザイン調整（ボタンの見た目だけ）
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        height: 60px;
        margin-bottom: 15px;
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
    
    # 画面を「1 : 2 : 1」に分割（真ん中の「2」の場所にボタンを置く作戦）
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
    
    # サイドバー（メニューに戻るボタン）
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

        # 問題画面
        else:
            target = cards[idx]

            # 1. ヘッダー（第○問）
            st.markdown(f"<h3 style='text-align: center;'>第 {idx + 1} 問</h3>", unsafe_allow_html=True)
            st.write("") # 少し隙間

            # 2. メインエリア（ここも 1:2:1 で真ん中に配置）
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # A. 答えを見る前
                if not st.session_state.show_answer:
                    if os.path.exists(target['filename']):
                        # ★ここ修正：サイズを数値で指定（これが一番安全です）
                        st.image(target['filename'], width=300)
                    else:
                        st.error(f"画像なし: {target['filename']}")
                    
                    # 隙間
                    st.write("")
                    
                    if st.button("答えを見る"):
                        st.session_state.show_answer = True
                        st.rerun()

                # B. 答えを見た後
                else:
                    # 正解の文字
                    st.markdown(f"<h1 style='text-align: center; font-size: 60px; margin: 20px 0;'>{target['answer']}</h1>", unsafe_allow_html=True)
                    
                    if st.button("次の問題へ", type="primary"):
                        st.session_state.current_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
