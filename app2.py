import streamlit as st
import random
import os

# ページの設定
st.set_page_config(layout="centered")

# --- CSS設定（強力な真ん中寄せ & 余白調整）---
st.markdown("""
    <style>
    /* 1. 画面上部の余白をガッツリ空ける（これで文字切れを防ぐ） */
    .block-container {
        padding-top: 100px !important; /* 上に100pxの隙間を作る */
        padding-bottom: 50px !important;
        max-width: 500px !important;   /* スマホっぽく幅を狭く固定 */
    }

    /* 2. 画像を強制的に真ん中へ */
    div[data-testid="stImage"] {
        display: flex;
        justify_content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
    }

    /* 3. ボタンを強制的に真ん中へ */
    .stButton {
        display: flex;
        justify_content: center !important;
        margin: 0 auto !important;
    }

    /* 4. ボタン自体のデザイン */
    .stButton button {
        width: 100%;
        max-width: 300px;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* 5. 文字をすべて真ん中揃えに */
    h1, h2, h3, p, div {
        text-align: center !important;
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
