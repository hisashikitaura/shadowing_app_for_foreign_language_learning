import streamlit as st
import openai

import os
from pathlib import Path
import re
from dotenv import load_dotenv
import dotenv
import uuid
import time

from llms.utils import use_openai_gpt_4o_mini, use_nvidia_nim_meta_llama_3_2_3b_instruct, use_nvidia_guardrails
from services.text_to_speech import run_openai_tts, run_nvidia_fastpitch_hifigan_tts
from utils.utils import show_text

# model
OPENAI_GPT_4O_MINI = "OpenAI/gpt-4o-mini"
NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT = "NVIDIA NIM/meta/llama-3.2-3b-instruct"
NVIDIA_NIM_GUARDRAILS = "NVIDIA Guardrails"

model = NVIDIA_NIM_GUARDRAILS

load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))
file_save_path = Path("__file__").parent / "speeches"

st.set_page_config(page_title ="🐶🐶Shadowing App")
st.title('🐶🐶Shadowing🐶🐶')
st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)



def get_uuid() -> str:
  """
  Get a unique id.
  This id is used for the folder and the file name.
  """
  return str(uuid.uuid4())


def create_path(base_path:str, dir_name:str="temp") -> str:
  """
  Create a directory for saving your favorite shadowing files.
  """
  path_joined = os.path.join(base_path, dir_name)
  try:
    if not os.path.exists(path_joined):
      os.makedirs(path_joined)
  except OSError:
    print("Error: Creating directory. " + path_joined)
  return path_joined



def generate_text(language_name="English", topic="Foods", num_sentences=5, level="Beginner", model=NVIDIA_NIM_GUARDRAILS) -> str:
  """
  Generate text for shadowing practice.
  """
  if model == OPENAI_GPT_4O_MINI:
    text = use_openai_gpt_4o_mini(language_name, topic, num_sentences, level)
  elif model == NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT:
    text = use_nvidia_nim_meta_llama_3_2_3b_instruct(language_name, topic, num_sentences, level)
  elif model == NVIDIA_NIM_GUARDRAILS:
    text = use_nvidia_guardrails(language_name, topic, num_sentences, level)    
  else:
    st.error("😩Please select a model.😩", "😩")

  return text


def create_voice_file(text:str, path:str=None, uuid:int=0) -> None:
  """
  Create speech with TTS model.
  This function is for one sentence.
  """
  print("Creating voice file...")
  # split the text into sentences
  sentences = []
  sentences = re.findall('<p>(.*?)</p>', text)
  
  file_save_path = create_path(path, uuid)

  for i, s in enumerate(sentences):
    resonse = run_nvidia_fastpitch_hifigan_tts(s, file_save_path, i)


def store_text(text:str, uuid:str=None):
  """
  Save the generated text to database.

  """
  print("Storing text...")
  pass


with st.form('🐮Foreign Language Sentence Generator🐮'):
  language_name = st.selectbox(
    "🐰What Languages do you learn?🐰 :",
    # ("Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh"),
      ("English", "French", "German", "Italian", "Spanish", "Chinese"),
  )
  topic = st.text_input('🐻What topics interest you?🐻 :', 'Foods')
  num_sentences = st.selectbox(
    "🐱How many sentences do you read aloud?🐱 :", ("3", "5", "10", "15", "20")
  )
  level = st.selectbox(
    "🐵What is your skill level?🐵 :",
    ("Beginner", "Elementary", "Intermediate", "Upper Intermediate", "Advanced", "Proficiency"),
  )

  if "user" not in st.session_state:
      # "create_voice_flag":  whether this program creates a voice file or not.
    st.session_state.user = {"language_name": language_name, "topic": topic, "level": level, "text": None}
  else:
    st.session_state.user["language_name"] = language_name
    st.session_state.user["topic"] = topic
    st.session_state.user["level"] = level

  # **************************************************************************************************
  
  st.divider()
  st.write("🥷🏽FOR DEVELOPER SETTINGS🥷🏽")
  
  # guardrails = True
  guardrails = st.toggle("🦸🏼‍♀️[Optional] Do you want to use guardrails?🦸🏼‍♀️", True)
  print(guardrails)
  if not guardrails:
    model = st.selectbox(
      "🦹🏼‍♂️[Optional] Which model do you use?🦹🏼‍♂️ :",
      (NVIDIA_NIM_GUARDRAILS, OPENAI_GPT_4O_MINI, NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT),
    )

  submitted = st.form_submit_button('Submit')
  if submitted:
    text = generate_text(language_name, topic, num_sentences, level, model)

    if text == "I'm not sure what to say." or text == "I'm sorry, I can't respond to that.":
      st.error("😩Please try again.😩", "😩")
      st.stop()

    if "flag" not in st.session_state:
      # "create_voice_flag":  whether this program creates a voice file or not.
      st.session_state.flag = {"create_voice_flag": False}
    else:
      st.session_state.flag["create_voice_flag"] = False

    if not st.session_state.flag["create_voice_flag"]:
      show_text(text)
    print("create_voice_flag: ", st.session_state.flag["create_voice_flag"])

    st.session_state.user["text"] = text

  if "flag" not in st.session_state:
    pass
  elif st.session_state.flag["create_voice_flag"]:
    uuid = get_uuid()
    text = st.session_state.user["text"]
    topic = st.session_state.user["topic"]
    level = st.session_state.user["level"]
    create_voice_file(text, file_save_path, uuid)
    store_text(topic, level, text, uuid)

 