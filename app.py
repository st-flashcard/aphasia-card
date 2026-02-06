import streamlit as st
import random
import os

# ページの設定（スマホでも見やすくする）
st.set_page_config(layout="centered")

# CSSで「ボタンを右寄せ」「文字を真ん中」にするための魔法のデザイン設定
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 50px;
    }
    .right-align {
        display: flex;
        justify_content: flex-end;
    }
    .center-align {
        display: flex;
        justify_content: center;
        align-items: center;
        height: 300px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. データの準備（画像ファイル名を確認してね！）
# GitHubにアップするときは、画像ファイルも一緒に入れます
cards_data = [
    {"filename": "/apple.jpg", "answer": "りんご"},
    {"filename": "/cat.jpg",   "answer": "ねこ"},
    {"filename": "/pen.jpg",   "answer": "ぺん"},
]

# 2. アプリの状態を管理する（Streamlit特有の書き方）
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
        # リセット処理
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
    # 答えを見る前（画像表示）
    if not st.session_state.show_answer:
        col1, col2, col3 = st.columns([1, 6, 1]) # 真ん中を広くするレイアウト
        with col2:
            # 画像があるかチェックして表示
            if os.path.exists(target['filename']):
                st.image(target['filename'], use_container_width=True)
            else:
                st.error(f"画像が見つかりません: {target['filename']}")
        
        # スペースを空ける
        st.write("") 

        # ③ ボタン（右下：答えを見る）
        # 列を作って右側にボタンを置くテクニック
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("答えを見る"):
                st.session_state.show_answer = True
                st.rerun()

    # 答えを見た後（正解表示）
    else:
        # 正解をど真ん中に表示
        st.markdown(f"""
        <div class='center-align'>
            <h1 style='font-size: 60px; margin: 0;'>{target['answer']}</h1>
        </div>
        """, unsafe_allow_html=True)

        # スペース
        st.write("")

        # ③ ボタン（右下：次の問題へ）
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("次の問題へ", type="primary"): # 緑っぽい色になる
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
