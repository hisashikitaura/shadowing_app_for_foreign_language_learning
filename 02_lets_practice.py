import streamlit as st
import openai

import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

from llms.utils import use_openai_gpt_4o_mini, use_nvidia_nim_meta_llama_3_2_3b_instruct, use_nvidia_guardrails, generate_text
from services.text_to_speech import run_openai_tts, run_nvidia_fastpitch_hifigan_tts, create_voice_file
from utils.utils import show_text, create_path, get_uuid
from store.store import store_text, store_user_preference
from config import Config

load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))
file_save_path = Path("__file__").parent / "store"

st.title('🐶🐶Shadowing🐶🐶')
st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)

df = pd.read_csv(f"{file_save_path}/{Config.USER_PREFERENCE_FILE}")
df = df.set_axis(["topic", "level", "uuid", "gender", "emotion", "first_sentence"], axis=1)

event = st.dataframe(
    df,
    key="data",
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "topic": st.column_config.TextColumn("Topic"),
        "level": st.column_config.TextColumn("Level"),
        "uuid": None,
        "gender": st.column_config.TextColumn("Gender"),
        "emotion": st.column_config.TextColumn("Emotion"),
        "first_sentence": st.column_config.TextColumn("First Sentence"),
    },
    hide_index=True,    
)

event.selection