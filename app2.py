import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# CSS設定（デザイン調整）
st.markdown("""
    <style>
    /* ボタンを大きくする */
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
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 1. データの準備（ここでコースを分けます）
# ----------------------------------------

# コースA：基本の単語（今までのやつ）
course_basic = [
    {"filename": "apple.jpg", "answer": "りんご"},
    {"filename": "cat.jpg",   "answer": "ねこ"},
    {"filename": "pen.jpg",   "answer": "ぺん"},
    {"filename": "watch.jpg", "answer": "とけい"},
    {"filename": "book.jpg",  "answer": "ほん"},
]

# コースB：動物カテゴリー（写真で見せてくれた内容を入れました！）
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

# 「今どの画面にいるか？」を管理する変数（menu = メニュー画面, game = ゲーム画面）
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ----------------------------------------
# 3. 画面の表示（条件分岐）
# ----------------------------------------

# ■ パターン1：メニュー画面（最初に表示される）
if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    st.write("") # スペース
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ボタンA
        if st.button("🍎 基本の単語"):
            st.session_state.card_list = course_basic.copy() # リストをコピー
            random.shuffle(st.session_state.card_list)       # シャッフル
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = 'game' # ゲーム画面へ移動
            st.rerun()

    with col2:
        # ボタンB
        if st.button("🐶 動物カテゴリー"):
            st.session_state.card_list = course_animals.copy()
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = 'game' # ゲーム画面へ移動
            st.rerun()

# ■ パターン2：ゲーム画面（訓練中）
elif st.session_state.mode == 'game':
    
    # 便利な変数を作る
    idx = st.session_state.current_index
    cards = st.session_state.card_list

    # --- 左上に「メニューに戻る」ボタンを設置 ---
    if st.button("← メニューに戻る", type="secondary"):
        st.session_state.mode = 'menu'
        st.rerun()
        
    st.divider() # 線を引く

    # --- 終了判定 ---
    if idx >= len(cards):
        st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
        if st.button("もう一度同じコースをやる"):
            random.shuffle(cards)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()

    # --- 問題表示 ---
    else:
        target = cards[idx]

        # ヘッダー
        st.markdown(f"<div style='text-align: left; font-size: 18px; font-weight: bold;'>第 {idx + 1} 問</div>", unsafe_allow_html=True)
        st.write("") 

        # A. 画像を表示
        if not st.session_state.show_answer:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if os.path.exists(target['filename']):
                    st.image(target['filename'], width=350) # サイズ固定
                else:
                    st.error(f"画像なし: {target['filename']}")
            
            st.write("") 
            
            # 答えボタン
            c1, c2 = st.columns([1, 1])
            with c2:
                if st.button("答えを見る"):
                    st.session_state.show_answer = True
                    st.rerun()

        # B. 正解を表示
        else:
            st.markdown(f"""
            <div style="text-align: center; width: 100%;">
                <h1 style="font-size: 80px; margin-top: 30px; margin-bottom: 30px;">
                    {target['answer']}
                </h1>
            </div>
            """, unsafe_allow_html=True)

            # 次へボタン
            c1, c2 = st.columns([1, 1])
            with c2:
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.rerun()
