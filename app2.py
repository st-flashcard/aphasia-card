import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# --- CSS設定（安全なデザインに書き直しました）---
st.markdown("""
    <style>
    /* 1. 画面上部の余白（文字切れ防止） */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
    }

    /* 2. 画像を真ん中に配置 */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center;
        align-items: center;
    }

    /* 3. ボタンを真ん中に配置 */
    .stButton {
        display: flex;
        justify_content: center;
    }

    /* 4. ボタン自体のデザイン */
    .stButton button {
        width: 100%;
        max-width: 300px;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 1. データの準備
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
# 2. アプリの状態管理
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
    # タイトルをHTMLで書いて真ん中寄せ
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>訓練メニューを選んでください</h2>", unsafe_allow_html=True)
    
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

    if not st.session_state.card_list:
        st.error("データがありません。メニューに戻ってください。")
        if st.button("戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        idx = st.session_state.current_index
        cards = st.session_state.card_list

        # 終了判定
        if idx >= len(cards):
            st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
            st.write("")
            if st.button("メニューに戻る"):
                st.session_state.mode = 'menu'
                st.rerun()

        # 問題表示
        else:
            target = cards[idx]

            # 文字切れ防止のためのクッション（透明な箱）を置きます
            st.write("")
            st.write("")

            # 第○問（HTMLで真ん中寄せ）
            st.markdown(f"<h3 style='text-align: center; margin-bottom: 20px;'>第 {idx + 1} 問</h3>", unsafe_allow_html=True)

            # A. 画像を表示
            if not st.session_state.show_answer:
                if os.path.exists(target['filename']):
                    # 幅を300pxにして表示
                    st.image(target['filename'], width=300)
                else:
                    st.error(f"画像なし: {target['filename']}")
                
                # 少し隙間
                st.write("") 
                
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

            # B. 正解を表示
            else:
                # 正解文字（HTMLで真ん中寄せ）
                st.markdown(f"""
                <div style="text-align: center; width: 100%;">
                    <h1 style="font-size: 80px; margin-top: 20px; margin-bottom: 30px;">
                        {target['answer']}
                    </h1>
                </div>
                """, unsafe_allow_html=True)

                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
