import streamlit as st

from config import Config

"""


What is feeling?NEW_LINE
Listen to the sample voice! ▶️

"""
"""
👩‍🦰 ✖️ 😐
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_FEMALE_1}.mp3", format=Config.AUDIO_MPEG, loop=False)
"""
👩‍🦰 ✖️ 🥰
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_FEMALE_HAPPY}.mp3", format=Config.AUDIO_MPEG, loop=False)
"""
👩‍🦰 ✖️ 😴
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_FEMALE_CALM}.mp3", format=Config.AUDIO_MPEG, loop=False)  
"""
👩‍🦰 ✖️ 😡
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_FEMALE_ANGRY}.mp3", format=Config.AUDIO_MPEG, loop=False)  
"""
👩‍🦰 ✖️ 😑
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_FEMALE_NEUTRAL}.mp3", format=Config.AUDIO_MPEG, loop=False)  
"""
NEW_LINE
NEW_LINE
👨‍🦰 ✖️ 😐
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_MALE_1}.mp3", format=Config.AUDIO_MPEG, loop=False)
"""
👨‍🦰 ✖️ 🥰
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_MALE_HAPPY}.mp3", format=Config.AUDIO_MPEG, loop=False)
"""
👨‍🦰 ✖️ 😴
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_MALE_CALM}.mp3", format=Config.AUDIO_MPEG, loop=False)  
"""
👨‍🦰 ✖️ 😡
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_MALE_ANGRY}.mp3", format=Config.AUDIO_MPEG, loop=False)  
"""
👨‍🦰 ✖️ 😑
"""
st.audio(f"{Config.SAMPLE_VOICE}\{Config.VOICE_ENG_MALE_NEUTRAL}.mp3", format=Config.AUDIO_MPEG, loop=False)  
