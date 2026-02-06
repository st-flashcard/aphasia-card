import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# CSS設定（ボタンの幅だけ調整）
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. データの準備
cards_data = [
    {"filename": "apple.jpg", "answer": "りんご"},
    {"filename": "cat.jpg",   "answer": "ねこ"},
    {"filename": "pen.jpg",   "answer": "ぺん"},
]

# 2. アプリの状態管理
if 'card_list' not in st.session_state:
    random.shuffle(cards_data)
    st.session_state.card_list = cards_data
    st.session_state.current_index = 0
    st.session_state.show_answer = False

idx = st.session_state.current_index
cards = st.session_state.card_list

# --- 画面表示 ---

# 終了画面
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

    # ① ヘッダー（左上）
    st.markdown(f"<div style='text-align: left; font-size: 18px; font-weight: bold;'>第 {idx + 1} 問</div>", unsafe_allow_html=True)
    
    # 余白
    st.write("") 

    # ② メインコンテンツ（中央）
    
    # A. 画像を表示するとき
    if not st.session_state.show_answer:
        # 3つの列を作って、真ん中（col2）に画像を置く
        col1, col2, col3 = st.columns([1, 10, 1])
        with col2:
            if os.path.exists(target['filename']):
                st.image(target['filename'], use_container_width=True)
            else:
                st.error("画像なし")
        
        st.write("") 
        
        # ボタン（右下）
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("答えを見る"):
                st.session_state.show_answer = True
                st.rerun()

    # B. 正解を表示するとき
    else:
        # ★ここを修正：一番シンプルな「強制中央揃え」にしました
        st.markdown(f"""
        <div style="text-align: center; width: 100%;">
            <h1 style="font-size: 80px; margin-top: 50px; margin-bottom: 50px;">
                {target['answer']}
            </h1>
        </div>
        """, unsafe_allow_html=True)

        # ボタン（右下）
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("次の問題へ", type="primary"):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
