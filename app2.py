import streamlit as st
import random
import os
import data  # ★ここで「倉庫（data.py）」を使えるようにしています

# 1. ページの設定
st.set_page_config(layout="centered", page_title="ことばの訓練")

# 2. デザインの調整 (CSS)
st.markdown("""
    <style>
    .main { background-color: #FFFFFF !important; color: #000000 !important; }
    /* ボタンを大きく見やすく */
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

# 3. 状態管理
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# 4. 画面表示
if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍎 基本"):
            # ★ここ重要！ data. をつけて呼び出します
            st.session_state.card_list = data.course_basic.copy()
            st.session_state.mode = 'game'
            st.rerun()
            
    with col2:
        if st.button("🐶 動物 1"):
            st.session_state.card_list = data.course_animals_1.copy()
            st.session_state.mode = 'game'
            st.rerun()

    with col3:
        if st.button("🐨 動物 2"):
            st.session_state.card_list = data.course_animals_2.copy()
            st.session_state.mode = 'game'
            st.rerun()

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
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        st.markdown(f"<p style='text-align: center;'>第 {idx + 1} 問 / {len(cards)} 問</p>", unsafe_allow_html=True)

        if not st.session_state.show_answer:
            if os.path.exists(target['filename']):
                st.image(target['filename'], width=250)
            else:
                st.error(f"画像が見つかりません: {target['filename']}")
            
            st.write("")
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()
        else:
            st.markdown(f"<div class='answer-text'>{target['answer']}</div>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1, 2, 1])
            with n2:
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
