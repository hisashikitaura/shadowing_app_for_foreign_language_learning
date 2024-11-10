import streamlit as st

import os
from pathlib import Path
from dotenv import load_dotenv

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
st.title('🐶🐶Let\'s do Shadowing!🐶🐶')
st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)


pg = st.navigation([st.Page("01_lets_generate.py", title="🐣Let\'s generate!🐣", icon=None, default=True),
                    st.Page("02_lets_choose.py", title="🐤Let\'s choose!🐤", icon=None, default=False),
                    st.Page("03_lets_do_shadowing.py", title="🐔Let\'s do Shadowing!🐔", icon=None, default=False),
                    st.Page("99_sample_voice.py", title="👄👄Sample Voice👄👄", icon=None, default=False)])
pg.run()




 