import streamlit as st
import random
import os

# 1. ページの設定
st.set_page_config(layout="centered")

# 2. デザイン調整（CSSで真ん中に寄せる作戦）
# カラムを使わず、この設定だけで真ん中に寄せます
st.markdown("""
    <style>
    /* 画像を真ん中に寄せる */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center;
    }
    
    /* ボタンを真ん中に寄せる */
    .stButton {
        display: flex;
        justify_content: center;
    }
    
    /* ボタンの大きさと見た目 */
    .stButton button {
        width: 300px; /* 幅を固定 */
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* 文字を真ん中に寄せる */
    h1, h2, h3, p {
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

# ----------------------------------------
# 画面の表示
# ----------------------------------------

# ■ パターン1：メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("<h2>訓練メニューを選んでください</h2>", unsafe_allow_html=True)
    st.write("") # スペース
    
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
    
    # サイドバー
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
            st.markdown("<h2>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
            if st.button("メニューに戻る"):
                st.session_state.mode = 'menu'
                st.rerun()

        # 問題表示画面
        else:
            target = cards[idx]

            # 1. 第○問
            st.markdown(f"<h3>第 {idx + 1} 問</h3>", unsafe_allow_html=True)
            st.write("")

            # A. 答えを見る前
            if not st.session_state.show_answer:
                if os.path.exists(target['filename']):
                    # CSSで中央になるので、そのまま表示（幅は300px）
                    st.image(target['filename'], width=300)
                else:
                    # 画像がない場合のエラー表示
                    st.error(f"画像が見つかりません: {target['filename']}")
                
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

            # B. 答えを見た後
            else:
                # 正解の文字
                st.markdown(f"<h1 style='font-size: 60px; margin: 30px 0;'>{target['answer']}</h1>", unsafe_allow_html=True)
                
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
