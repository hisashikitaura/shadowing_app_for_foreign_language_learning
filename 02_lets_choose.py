import streamlit as st

import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

from utils.utils import get_text_from_store, get_num_sentences
from config import Config

load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))
file_open_path = Path(__file__).parent / "store"
print(f"file_open_path: {file_open_path}")

st.title('🐶🐶Let\'s do Shadowing🐶🐶')
st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)

df = pd.read_csv(f"{file_open_path}/{Config.USER_PREFERENCE_FILE}", header=None, names=["topic", "level", "uuid", "gender", "emotion", "first_sentence"])
# df = df.set_axis(["topic", "level", "uuid", "gender", "emotion", "first_sentence"], axis=1)
print(f"df: {df}")
"😏Which topic do you want to do?😏"
"🤩Choose & Do Shadowing🤩"

event = st.dataframe(
    df,
    key="data",
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "topic": st.column_config.TextColumn("Topic"),
        "level": st.column_config.TextColumn("Level"),
        "uuid": None,
        "gender": st.column_config.TextColumn("Teacher's Gender"),
        "emotion": st.column_config.TextColumn("Teacher's Emotion"),
        "first_sentence": st.column_config.TextColumn("One of the Sentences"),
    },
    hide_index=True,    
)

if st.button("Go!", type="primary"):
    try:
        if "shadowing" not in st.session_state:
            st.session_state.shadowing = {"uuid": None, "file_open_path": file_open_path, "text": None, "num_sentences": None, "i_sentences": 0, "status": "do_shadowing_1"}
        else:
            st.session_state.shadowing["uuid"] = None
            st.session_state.shadowing["file_open_path"] = file_open_path
            st.session_state.shadowing["text"] = None
            st.session_state.shadowing["num_sentences"] = None
            st.session_state.shadowing["i_sentences"] = 0
            st.session_state.shadowing["status"] = "do_shadowing_1"

        row_num = event.selection.rows[0]
        uuid = df.iloc[row_num, 2] # uuid column = 2
    except Exception as e:
        print(f"Error: {e}")
        st.error("Error: Please select a row.")
        st.stop()

    st.session_state.shadowing["uuid"] = uuid
    st.session_state.shadowing["text"] = get_text_from_store(uuid, file_open_path)
    st.session_state.shadowing["num_sentences"] = get_num_sentences(st.session_state.shadowing["text"])

    st.switch_page("03_lets_do_shadowing.py")
