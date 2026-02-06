import streamlit as st
import random
import os

# ページの設定（スマホでも見やすくする）
st.set_page_config(layout="centered")

# CSSでデザインを調整
st.markdown("""
    <style>
    /* ボタンのサイズ調整 */
    .stButton button {
        width: 100%;
        height: 50px;
    }
    
    /* ★修正ポイント：文字を強制的にど真ん中に持ってくる設定 */
    .center-text {
        display: flex;
        justify_content: center; /* 横方向の真ん中 */
        align_items: center;     /* 縦方向の真ん中 */
        text-align: center;
        width: 100%;             /* 画面の横幅いっぱい使う */
        height: 300px;           /* 高さを確保 */
    }
    
    .right-align {
        display: flex;
        justify_content: flex-end;
    }
    </style>
""", unsafe_allow_html=True)

# 1. データの準備
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

# 変数を短くしておく
idx = st.session_state.current_index
cards = st.session_state.card_list

# --- 画面表示スタート ---

# 終了判定
if idx >= len(cards):
    st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
    st.write("すべてのカードが終わりました。")
    if st.button("もう一度やる"):
        random.shuffle(cards_data)
        st.session_state.card_list = cards_data
        st.session_state.current_index = 0
        st.session_state.show_answer = False
        st.rerun()

else:
    target = cards[idx]

    # ① ヘッダー（左上：第○問）
    st.markdown(f"<div style='text-align: left; font-size: 18px; font-weight: bold;'>第 {idx + 1} 問</div>", unsafe_allow_html=True)

    # ② メインコンテンツ（中央）
    
    # パターンA：答えを見る前（画像表示）
    if not st.session_state.show_answer:
        # 画像を真ん中に寄せるために3つの列を作る（左・中・右）
        col1, col2, col3 = st.columns([1, 10, 1]) 
        with col2:
            if os.path.exists(target['filename']):
                st.image(target['filename'], use_container_width=True)
            else:
                st.error(f"画像エラー: {target['filename']}")
        
        st.write("") # スペース

        # ボタン（右下：答えを見る）
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("答えを見る"):
                st.session_state.show_answer = True
                st.rerun()

    # パターンB：答えを見た後（正解表示）
    else:
        # 正解をど真ん中に表示（CSSクラス .center-text を適用）
        st.markdown(f"""
        <div class='center-text'>
            <h1 style='font-size: 80px; margin: 0;'>{target['answer']}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.write("") # スペース

        # ボタン（右下：次の問題へ）
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("次の問題へ", type="primary"):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
