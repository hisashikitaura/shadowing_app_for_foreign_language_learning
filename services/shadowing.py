import streamlit as st

import os
from pathlib import Path
from dotenv import load_dotenv
import time

import pygame

from utils.utils import stream_data, get_sentences

load_dotenv()

@st.dialog("😏Are you ready??😏")
def do_shadowing_1():
    """
    Do shadowing with the selected text.
    """
    sentences = get_sentences(st.session_state.shadowing["text"])
    for s in sentences:    
        st.write_stream(stream_data(s, 0.01))
    
    if st.button("Go ahead!", type="primary"):
        st.session_state.shadowing["status"] = "do_shadowing_2"
        st.rerun()


@st.dialog("😏Let's do it!!😏")
def do_shadowing_2() -> None:
    """
    Do shadowing with the selected text.
    """
    sentences = get_sentences(st.session_state.shadowing["text"])
    s = sentences[st.session_state.shadowing["i_sentences"]]
    print(f"s: {s}")
    colored_text = st.session_state.shadowing["text"].replace(f"<p>{s}</p>", f"<p><h2><b><font color=\"red\">{s}</font></b></h2></p>")
    print(f"colored_text: {colored_text}")
    st.html(colored_text)
    for _ in range(3):
        play_voice()
        time.sleep(3)
    st.session_state.shadowing["i_sentences"] += 1
    st.rerun()


def play_voice() -> None:
    file_open_path = st.session_state.shadowing["file_open_path"]
    uuid = st.session_state.shadowing["uuid"]
    i_sentences = st.session_state.shadowing["i_sentences"]
    file_path = f"{file_open_path}/{uuid}/{i_sentences}.wav"
    print(f"file_path: {file_path}")
    print("play_voice start")
    if not os.path.isfile(file_path):
        print(f"{file_path} is not a file")
        return
    
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    print("play_voice before while")   
    # Optional: wait for the music to finish playing
    while pygame.mixer.music.get_busy():
         pygame.time.Clock().tick(10)
                