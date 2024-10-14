import streamlit as st
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate

import os
from pathlib import Path
import re
from dotenv import load_dotenv
import uuid
import time

import openai

load_dotenv()

openai_api_key = str(os.getenv("OPENAI_API_KEY"))
file_save_path = Path("__file__").parent / "speeches"

st.set_page_config(page_title ="🐶🐶Shadowing App")
st.title('🐶🐶Shadowing🐶🐶')
st.logo(image="./image/dog.png", size="medium", link=None, icon_image=None)
# openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')



def get_id():
  """
  Get a unique id.
  This id is used for the folder and the file name.
  """
  return str(uuid.uuid4())



def create_path(base_path:str, dir_name:str="temp"):
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



def generate_text(language_name="English", topic="Foods", num_sentences=5, level="Beginner"):
  """
  Generate text for shadowing practice.
  """
  ASSISTANT = "assistant:"
  llm = ChatMessage(model='gpt-4o-mini',
                   temperature=0.8,
                   max_tokens=None,
                   timeout=None,
                   max_retries=2,
                   openai_api_key=openai_api_key)
  template = '''
              I will make a shadowing practice app for {language_name} Language Learners.
              In shadowing practice, a teacher (may be a computer) reads a {language_name} sentence by sentence aloud, and learners repeat at the same pace, with a slight delay if possible.
              
              As for the {language_name} materials, generate {language_name} text for {language_name} Language Learners.
                -- Topic: {topic}
                -- Number of the sentences: Approx. {num_sentences}                
                -- Skill level: {level}, defined by the Common European Framework of Reference for Languages (CEFR)
              Just the text. No words needed.
              No numbering at the beginning of the sentences.
              Enclose each sentence in <p> tag.
              '''

  qa_template = PromptTemplate(template)
  prompt = qa_template.format(language_name=language_name, topic=topic, num_sentences=num_sentences, level=level)
  messages = [
              ChatMessage(role="system", content="You're a text generator that a user wants. No talks."),
              ChatMessage(role="user", content=prompt)
            ]
  res_text = OpenAI().chat(messages)
  return str(res_text).replace(ASSISTANT, "").strip()



def create_speech(text:str):
  """
  Create speech with TTS model.
  This function is for one sentence.
  """
  # split the text into sentences
  sentences = []
  sentences = re.findall('<p>(.*?)</p>', text)
  
  id = get_id()
  file_save_path = create_path(file_save_path, id)

  for i, s in enumerate(sentences):
    """
    openai/resouces/audio/speech.py
    """
    with openai.audio.speech.with_streaming_response.create(
      model="tts-1",
      voice="nova", #'nova', 'shimmer', 'echo', 'onyx', 'fable' or 'alloy'
      input=s,
      speed=1,
    ) as response:
      try:
        response.stream_to_file(f"{file_save_path}/{i}_.mp3")
      except Exception as e:
        st.error(e)



@st.dialog("The shadowing practice text")
def show_text(text):
  """
  This shows modal dialog with the generated text.
  And a user has to choose one.
  """
  st.html(text)
  if st.button("OK"):
    st.balloons()
    time.sleep(2)
    st.success("Let's practice!", icon="👍")
    create_speech(text)
  if st.button("Cancel"):
    st.info("Don't go away and let's practice!", icon="👍")
    st.rerun()    




with st.form('Foreign Language Sentence Generator'):
  language_name = st.selectbox(
    "What Languages do you learn? :",
    # ("Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh"),
      ("English", "French", "German", "Italian", "Spanish", "Chinese"),
  )
  topic = st.text_input('What topics interest you? :', 'Foods')
  num_sentences = st.selectbox(
    "How many sentences do you read aloud? :", ("3", "5", "10", "15", "20")
  )
  level = st.selectbox(
    "Your skill level:",
    ("Beginner", "Elementary", "Intermediate", "Upper Intermediate", "Advanced", "Proficiency"),
  )

  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key in the .env file!', icon='⚠')
  elif submitted:
    st.divider()
    text = generate_text(language_name, topic, num_sentences, level)
    show_text(text)

 