import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# CSS設定（デザイン調整）
st.markdown("""
    <style>
    /* 全体の余白調整 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* 画像を強制的に真ん中に配置 */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center;
        align-items: center;
    }

    /* ボタンを強制的に真ん中に配置 */
    .stButton {
        display: flex;
        justify_content: center;
    }
    
    /* ボタン自体のデザイン */
    .stButton button {
        width: 100%;
        max-width: 300px;    /* スマホで見やすいサイズ */
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px; /* ボタン同士の間隔 */
    }

    /* タイトル文字 */
    .title-text {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    /* 第○問の文字 */
    .question-text {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #555;
        margin-bottom: 10px;
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
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    st.write("") # スペース
    
    # 基本の単語ボタン
    if st.button("🍎 基本の単語"):
        st.session_state.card_list = course_basic.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun() # ←ここにカッコ () があるのが正解です！

    st.write("") # スペース
    
    # 動物カテゴリーボタン
    if st.button("🐶 動物カテゴリー"):
        st.session_state.card_list = course_animals.copy()
        random.shuffle(st.session_state.card_list)
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.session_state.mode = 'game'
        st.rerun() # ←ここもカッコ () が必須！

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

    # エラー回避（データがない場合）
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

            # ヘッダー（第○問）
            st.markdown(f"<div class='question-text'>第 {idx + 1} 問</div>", unsafe_allow_html=True)

            # A. 画像を表示（答えを見る前）
            if not st.session_state.show_answer:
                if os.path.exists(target['filename']):
                    st.image(target['filename'], width=280) 
                else:
                    st.error(f"画像なし: {target['filename']}")
                
                st.write("") 
                
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

            # B. 正解を表示（答えを見た後）
            else:
                # 正解の文字
                st.markdown(f"""
                <div style="text-align: center; width: 100%;">
                    <h1 style="font-size: 80px; margin-top: 10px; margin-bottom: 20px;">
                        {target['answer']}
                    </h1>
                </div>
                """, unsafe_allow_html=True)

                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
