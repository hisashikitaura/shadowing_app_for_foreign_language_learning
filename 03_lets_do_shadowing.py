import streamlit as st

import os
from dotenv import load_dotenv

from services.shadowing import do_shadowing_1, do_shadowing_2


load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))

st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)

if st.session_state.shadowing["i_sentences"] < st.session_state.shadowing["num_sentences"]:
    if st.session_state.shadowing["status"] == "do_shadowing_1":
        do_shadowing_1()
    elif st.session_state.shadowing["status"] == "do_shadowing_2":
        do_shadowing_2()
else:
    st.success("🎉🎉Congratulations!! You've done all the shadowing!!🎉🎉")
    # st.switch_page("01_lets_generate.py")
