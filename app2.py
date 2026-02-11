import streamlit as st
import random
import os
import data  # ★ここで倉庫(data.py)を呼び出します!

# 1. ページの設定
st.set_page_config(layout="centered", page_title="ことばの訓練")

# 2. デザインの調整 (CSS)
st.markdown("""
    <style>
 /* アプリ全体を強制的に白くする */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* 基本の文字色を黒に */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #000000 !important;
    }
    /* ★ここが鉄壁ガード！右上のメニューやGithubアイコンを完全に消す */
    [data-testid="stToolbar"], 
    [data-testid="stHeader"], 
    [data-testid="stStatusWidget"], 
    #MainMenu, 
    footer {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
 /* 画像と文字の距離調整 */
    [data-testid="stImage"] {
        margin-top: -60px !important;    /* 上の隙間を削って文字に近づく */
        margin-bottom: -90px !important; /* 下の隙間を削ってボタンに近づく */
    }
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
    /* 正解文字のデザイン(色を黒に修正) */
    .answer-text {
        text-align: center;
        font-size: 80px;
        font-weight: bold;
        color: #000000; /* ★ここを黒に変更しました */
        margin: 20px 0;
    }

    /* ヒントのデザイン */
    .hint-container {
        text-align: center;
        font-size: 20px;           /* 「ヒント:」の文字サイズ */
        font-weight: bold;
        color: #555555 !important; /* 基本は少しグレー */
        margin-top: 20px;
        margin-bottom: 10px;
        display: flex;             /* 横並びにする */
        justify-content: center;   /* 中央寄せ */
        align-items: baseline;     /* 文字の底辺を揃える */
    }

    /* 特大の1文字目 */
    .hint-big-char {
        font-size: 60px;          /* ドーンと大きく! */
        color: #000000 !important; /* ここだけ真っ黒で強調 */
        margin-left: 15px;         /* 左に少し隙間 */
        margin-right: 5px;         /* 右に少し隙間 */
        line-height: 1;            /* 行間を詰める */
    }

    /* ボタンのデザイン */
    .stButton > button { 
        width: 100%; 
        height: 60px; 
        font-size: 18px; 
        font-weight: bold; 
        background-color: #FFFFFF !important; /* 背景は真っ白 */
        color: #000000 !important;            /* 文字は真っ黒 */
        border: 2px solid #CCCCCC !important; /* グレーの枠線をつける */
    }
    
    /* ボタンに触れた時やクリックした時も黒くならないようにする */
    .stButton > button:hover, .stButton > button:active, .stButton > button:focus {
        background-color: #F0F0F0 !important; /* 薄いグレー */
        color: #000000 !important;            /* 文字は黒のまま */
        border-color: #AAAAAA !important;
    }
    /* 画像を中央に固定する設定 */
    [data-testid="stImage"] img {
        display: block;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* ★★★ スマホでもボタンを横並びにする魔法 ★★★ */
    /* Streamlitのcolumnsをスマホでも横並びに強制する */
    [data-testid="column"] {
        min-width: 0 !important;
        flex: 1 1 0 !important;
    }
    
    /* メニューボタンエリアを横並びグリッドにする */
    .menu-button-row {
        display: flex !important;
        gap: 8px !important;
        margin-bottom: 15px !important;
    }
    
    .menu-button-row .stButton {
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    .menu-button-row .stButton button {
        font-size: 16px !important;
        height: 55px !important;
        padding: 8px 4px !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }
    
    /* カテゴリタイトルのスタイル */
    .category-title {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #000000 !important;
        margin: 20px 0 10px 0 !important;
        text-align: left !important;
    }
    
    /* スマホ対応: 小さい画面ではボタンの文字をさらに小さく */
    @media (max-width: 480px) {
        .menu-button-row .stButton button {
            font-size: 14px !important;
            height: 50px !important;
        }
        
        .category-title {
            font-size: 18px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 3. アプリの状態管理
# ----------------------------------------
if 'mode' not in st.session_state:
    st.session_state.mode = 'menu'
    st.session_state.card_list = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# ★ここが重要！後から追加した変数は、個別にチェックして作る必要があります
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
# ----------------------------------------
# 4. 画面表示のロジック
# ----------------------------------------

# ■ メニュー画面
if st.session_state.mode == 'menu':
    st.markdown("<div class='title-text'>訓練メニューを選んでください</div>", unsafe_allow_html=True)
    
    # === 動物エリア ===
    st.markdown("<div class='category-title'>🐶 動物</div>", unsafe_allow_html=True)
    st.markdown("<div class='menu-button-row'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("動物 1"):
            st.session_state.card_list = data.course_animals1.copy() 
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

    with col2:
        if st.button("動物 2"):
            st.session_state.card_list = data.course_animals2.copy()
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()

    with col3:
        if st.button("動物 3"):
            st.session_state.card_list = data.course_animals3.copy()
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # === 食べ物エリア ===
    st.markdown("<div class='category-title'>🥦 食べ物</div>", unsafe_allow_html=True)
    st.markdown("<div class='menu-button-row'>", unsafe_allow_html=True)
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        if st.button("野菜"):
            st.session_state.card_list = data.course_vegetables.copy()
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()
            
    with f_col2:
        if st.button("果物"):
            st.session_state.card_list = data.course_fruits.copy()
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # === 生活用品エリア ===
    st.markdown("<div class='category-title'>👓 生活</div>", unsafe_allow_html=True)
    st.markdown("<div class='menu-button-row'>", unsafe_allow_html=True)
    l_col1, l_col2 = st.columns(2)
    
    with l_col1:
        if st.button("身の回りのもの 1"):
            st.session_state.card_list = data.course_daily_items1.copy()  # ★修正！
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()
    with l_col2:
        if st.button("身の回りのもの 2"):
            st.session_state.card_list = data.course_daily_items2.copy()  # ★修正！
            st.session_state.mode = 'game'
            random.shuffle(st.session_state.card_list)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


# ■ ゲーム画面
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

    # 終了判定
    if idx >= len(cards):
        st.markdown("<h2 style='text-align: center;'>🎉 おつかれさまでした！</h2>", unsafe_allow_html=True)
        if st.button("メニューに戻る"):
            st.session_state.mode = 'menu'
            st.rerun()
    else:
        target = cards[idx]
        # ★ここを修正しました:z-indexを追加して文字を最前面に!
        st.markdown(f"<p style='text-align: center; margin-bottom: 0px; position: relative; z-index: 999;'>第 {idx + 1} 問 / {len(cards)} 問</p>", unsafe_allow_html=True)
        
        # 画像の表示(まだ正解を見ていない時)
        if not st.session_state.show_answer:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                if os.path.exists(target['filename']):
                    st.image(target['filename'], use_container_width=True)
                else:
                    st.error(f"画像が見つかりません: {target['filename']}")
            
            # ヒント表示エリア
            if st.session_state.show_hint:
                first_char = target['answer'][0]
                # 最初の文字だけに特別なクラス(hint-big-char)を適用します
                st.markdown(f"""
                    <div class='hint-container'>
                        ヒント: <span class='hint-big-char'>{first_char}</span> ...
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.write("")

            # ★ここが抜けていました!ボタンエリア復活★
            st.write("")
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                btn_left, btn_right = st.columns(2)
                
                with btn_left:
                    if st.button("答えを見る"):
                        st.session_state.show_answer = True
                        st.rerun()
                
                with btn_right:
                    if st.button("ヒント"):
                        st.session_state.show_hint = True
                        st.rerun()

        # 正解の表示(答えを見た後)
        else:
            st.markdown(f"<div class='answer-text'>{target['answer']}</div>", unsafe_allow_html=True)
            
            n1, n2, n3 = st.columns([1, 2, 1])
            with n2:
                if st.button("次の問題へ", type="primary"):
                    st.session_state.current_index += 1
                    st.session_state.show_answer = False
                    st.session_state.show_hint = False
                    st.rerun()
