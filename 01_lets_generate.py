import streamlit as st

import os
from pathlib import Path
from dotenv import load_dotenv

from llms.utils import generate_text
from services.text_to_speech import create_voice_file
from utils.utils import show_text, show_error, get_uuid
from services.store import store_text, store_user_preference
from config import Config

import validators.url

load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))
file_save_path = Path(__file__).parent / "store"
print(f"file_save_path: {file_save_path}")

# def if_rerun():

if "user" in st.session_state:
  previous_topic = st.session_state.user["topic"]
  previous_topic_url = st.session_state.user["topic_url"]
else:
  previous_topic = "Foods"
  previous_topic_url = None


with st.form('🐮🐮🐮Improve your foreign language skills🐮🐮🐮'):
  language_name = st.selectbox(
    "🐰🐰🐰What Languages??🐰🐰🐰 :　*English Only🙇🏼‍♂️🙇🏼‍♂️",
    # ("Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh"),
      ("English", "French", "German", "Italian", "Spanish", "Chinese"),
  )
  topic = st.text_input(label='🐻🐻🐻What topics??🐻🐻🐻 :', value=previous_topic)

  topic_url = None
  _topic_url = st.text_input(label="[Optional] From this website, the phrases on the topic can be extracted. *This may take a few minutes..", value=previous_topic_url, placeholder="www.nvidia.com/en-us/")
  if _topic_url is not None:
    if validators.url(_topic_url):
      topic_url = _topic_url
    else:
      topic_url = None
      st.warning("Your URL is not valid. Skip...")

  num_sentences = st.selectbox(
    "🐱🐱🐱How many sentences do you want??🐱🐱🐱 :", ("3", "5", "10", "15", "20")
  )

  level = st.selectbox(
    "🐵🐵🐵Your skill level??🐵🐵🐵 :",
    ("Beginner", "Intermediate", "Advanced"),
  )

  teacher = st.selectbox(
    "🩵🩵🩵Your teacher??🩵🩵🩵 :",
    ( "👩‍🦰", "👨‍🦰"),
    index=None,
    placeholder="what type?",
  )
  if teacher is None:
    teacher = "👩‍"
  
  emotion = st.selectbox(
      "🩵🩵🩵Teacher's feeling??🩵🩵🩵 :",
      ("😐", "🥰", "😴", "😡", "😑"),
      index=None,
      placeholder="what feeling?",
  )
  if emotion is None:
    emotion = "😐"

  if "user" not in st.session_state:
      # "create_voice_flag":  whether this program creates a voice file or not.
    st.session_state.user = {"language_name": language_name, "topic": topic, "topic_url": topic_url, "level": level, "text": None}
  else:
    st.session_state.user["language_name"] = language_name
    st.session_state.user["topic"] = topic
    st.session_state.user["topic_url"] = topic_url
    st.session_state.user["level"] = level

  # **************************************************************************************************
  
  # st.divider()
  # st.write("🥷🏽FOR DEVELOPER SETTINGS🥷🏽")
  
  # # guardrails = True
  # guardrails = st.toggle("🦸🏼‍♀️[Optional] Do you want to use guardrails?🦸🏼‍♀️", True)
  # print(guardrails)
  # if not guardrails:
  #   model = st.selectbox(
  #     "🦹🏼‍♂️[Optional] Which model do you use?🦹🏼‍♂️ :",
  #     (Config.NVIDIA_NIM_GUARDRAILS, Config.OPENAI_GPT_4O_MINI, Config.NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT),
  #   )

  submitted = st.form_submit_button('Submit')
  if submitted:
    print("before generate_text")
    text = generate_text(language_name, topic, topic_url, num_sentences, level, model=Config.NVIDIA_NIM_GUARDRAILS)
    print("after generate_text")

    if text == "I'm not sure what to say." or text == "I'm sorry, I can't respond to that.":
      show_error()
      st.stop()

    if "flag" not in st.session_state:
      # "create_voice_flag":  whether this program creates a voice file or not.
      st.session_state.flag = {"show_text": False, "create_voice_flag": False}
    else:
      st.session_state.flag["create_voice_flag"] = False

    if not st.session_state.flag["create_voice_flag"]:
      show_text(text)
    print("create_voice_flag: ", st.session_state.flag["create_voice_flag"])

    st.session_state.user["text"] = text

  if "flag" not in st.session_state:
    pass
  elif st.session_state.flag["create_voice_flag"]:
    print("elif st.session_state.flag")
    uuid = get_uuid()
    text = st.session_state.user["text"]
    topic = st.session_state.user["topic"]
    level = st.session_state.user["level"]
    create_voice_file(text, file_save_path, uuid, teacher, emotion)
    store_text(text, file_save_path, uuid)
    store_user_preference(text, file_save_path, topic, level, uuid, teacher, emotion)

    st.session_state.flag["show_text"] = False
    
    st.switch_page("02_lets_choose.py")

  st.divider()
  """
  What is teacher's feeling?
  Listen to the sample voice!
  """
  st.page_link("04_sample_voice.py", label="👄👄Sample Voice👄👄", icon=None)




 