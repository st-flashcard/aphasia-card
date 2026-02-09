import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# CSS設定（デザイン調整）
st.markdown("""
    <style>
    /* ボタンを大きく見やすく */
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    /* タイトル画面の文字 */
    .title-text {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* ★追加：画像自体を中央に寄せる設定 */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 1. データの準備（変更なし）
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
# 2. アプリの状態管理（変更なし）
# ----------------------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ----------------------------------------
# 3. 画面の表示
# ----------------------------------------

# ■ パターン1：メニュー画面
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

# ■ パターン2：ゲーム画面
elif st.session_state.mode == 'game':
    
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
        st.error("データがありません。メニューに戻ってください。")
        if st.button("戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        idx = st.session_state.current_index
        cards = st.session_state.card_list

        if idx >= len(cards):
            st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
            if st.button("メニューに戻る"):
                st.session_state.mode = 'menu'
                st.rerun()

        else:
            target = cards[idx]
            st.markdown(f"<div style='text-align: center; font-size: 18px; margin-bottom: 10px;'>第 {idx + 1} 問</div>", unsafe_allow_html=True)

            # A. 画像を表示
            if not st.session_state.show_answer:
                # 画像の表示（CSSにより、この col2 の中で中央寄せになります）
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if os.path.exists(target['filename']):
                        st.image(target['filename'], width=280) 
                    else:
                        st.error(f"画像が見つかりません: {target['filename']}")
                
                st.write("") 
                c1, c2, c3 = st.columns([1, 2, 1]) 
                with c2:
                    if st.button("答えを見る"):
                        st.session_state.show_answer = True
                        st.rerun()

            # B. 正解を表示
            else:
                st.markdown(f"""
                <div style="text-align: center; width: 100%;">
                    <h1 style="font-size: 80px; margin-top: 10px; margin-bottom: 20px;">
                        {target['answer']}
                    </h1>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    if st.button("次の問題へ", type="primary"):
                        st.session_state.current_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
