import streamlit as st
import random
import os

# ページの設定（スマホでも見やすくする）
st.set_page_config(layout="centered")

# --- CSSで「全部真ん中」にする強力な設定 ---
st.markdown("""
    <style>
    /* 1. 画像を強制的に真ん中へ */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center;
        align-items: center;
    }

    /* 2. ボタンの入れ物を真ん中へ */
    .stButton {
        display: flex;
        justify_content: center;
    }

    /* 3. ボタン自体のデザイン調整 */
    .stButton button {
        width: 300px; /* 幅を300pxに固定（スマホでもPCでも程よい） */
        max-width: 90%; /* 画面が狭すぎるときは90%まで縮む */
        height: 60px;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 1. データの準備
# ※ファイル名の先頭に "/" は不要です。同じフォルダにある前提です。
cards_data = [
    {"filename": "apple.jpg", "answer": "りんご"},
    {"filename": "cat.jpg",   "answer": "ねこ"},
    {"filename": "pen.jpg",   "answer": "ぺん"},
]

# 2. アプリの状態を管理
if 'card_list' not in st.session_state:
    random.shuffle(cards_data)
    st.session_state.card_list = cards_data
    st.session_state.current_index = 0
    st.session_state.show_answer = False

idx = st.session_state.current_index
cards = st.session_state.card_list

# --- 画面表示スタート ---

# 終了判定
if idx >= len(cards):
    st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
    st.write("")
    # ボタンもCSSで勝手に真ん中になります
    if st.button("もう一度やる"):
        random.shuffle(cards_data)
        st.session_state.card_list = cards_data
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.rerun()

else:
    target = cards[idx]

    # ① ヘッダー（ここを「center」に変更！）
    st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px;'>第 {idx + 1} 問</div>", unsafe_allow_html=True)

    # ② メインコンテンツ（中央）
    # 答えを見る前（画像表示）
    if not st.session_state.show_answer:
        # columns（列）は使いません。CSSで自動的に真ん中になります。
        if os.path.exists(target['filename']):
            # widthを指定して程よい大きさで表示
            st.image(target['filename'], width=300)
        else:
            st.error(f"画像が見つかりません: {target['filename']}")
        
        st.write("") # スペース

        # ③ ボタン（答えを見る）
        # こちらもcolumnsは不要です。
        if st.button("答えを見る"):
            st.session_state.show_answer = True
            st.rerun()

    # 答えを見た後（正解表示）
    else:
        # 正解をど真ん中に表示
        st.markdown(f"""
        <div style='text-align: center;'>
            <h1 style='font-size: 80px; margin: 30px 0;'>{target['answer']}</h1>
        </div>
        """, unsafe_allow_html=True)

        # ③ ボタン（次の問題へ）
        if st.button("次の問題へ", type="primary"):
            st.session_state.current_index += 1
            st.session_state.show_answer = False
            st.rerun()
