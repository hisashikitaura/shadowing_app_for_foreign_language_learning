import streamlit as st
import openai

import os
from pathlib import Path
from dotenv import load_dotenv

from llms.utils import use_openai_gpt_4o_mini, use_nvidia_nim_meta_llama_3_2_3b_instruct, use_nvidia_guardrails, generate_text
from services.text_to_speech import run_openai_tts, run_nvidia_fastpitch_hifigan_tts, create_voice_file
from utils.utils import show_text, create_path, get_uuid
from store.store import store_text, store_user_preference
from config import Config

load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))
file_save_path = Path("__file__").parent / "store"


st.set_page_config(
    page_title="🐶🐶Shadowing",
    page_icon="🌈",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.youtube.com',
        'Report a bug': "https://www.google.com",
        'About': "# Good Luck!"
    }
)
st.title('Let\'s do Shadowing!')
st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)


pg = st.navigation([st.Page("01_lets_generate.py", title="🐣Let\'s generate!🐣", icon=None, default=True),
                     st.Page("02_lets_practice.py", title="🐔Let\'s practice!🐔", icon=None, default=False),
                     st.Page("03_sample_voice.py", title="👄👄Sample Voice👄👄", icon=None, default=False)])
pg.run()




 