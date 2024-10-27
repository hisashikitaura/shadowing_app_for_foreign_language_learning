import streamlit as st

import os
import time
import shutil
import uuid
import re

from config import Config

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


@st.dialog("😏Try to listen!😏")
def play_voice():
  """
  This shows modal dialog with the generated text.
  And a user has to choose one.
  st.dial
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
  st.rerun() 

@st.dialog("😏Your favorite text??😏")
def show_text(text) -> bool:
  """
  This shows modal dialog with the generated text.
  And a user has to choose one.
  st.dialog function can't return a value.
  """
  print(f"show_text: start")
  _text = text.replace("<p>", "<p>💙")
  sentences = re.findall('<p>(.*?)</p>', _text)
  for s in sentences:
    st.write_stream(stream_data(s))
  print(f"show_text: end")

  if st.button("😍YES!😍", key=0):
    st.balloons()
    time.sleep(2)
    st.session_state.flag["create_voice_flag"] = True
    st.rerun()
  if st.button("🙄I'll try again🙄", key=1):
    st.session_state.flag["create_voice_flag"] = False     
    st.rerun()


@st.dialog("😩Bad Topic!😩")
def show_error() -> bool:
  """
  Submitted topic is not good.
  """
  st.error("😌😌😌Please change the topic😌😌😌")


def remove_ptag(text:str, emoji:bool=False) -> str:
  """
  Decorate the text.
  """
  if emoji:
    return text.replace("<p>", "💙").replace("</p>", f"{Config.NEW_LINE}")
  else:
    return text.replace("<p>", "").replace("</p>", f"{Config.NEW_LINE}")


def copy_multiple_files(file_list, destination_dir):
  results = []
  for file in file_list:
    success = copy_file_with_error_handling(file, destination_dir)
    results.append((file, success))
  return results


def copy_file_with_error_handling(source_file, destination_dir):
    try:
        # Check if source file exists
        if not os.path.exists(source_file):
            print(f"Source file {source_file} does not exist")
            return False
        
        # Check if source is a file
        if not os.path.isfile(source_file):
            print(f"{source_file} is not a file")
            return False
            
        # Create destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            
        # Check write permissions
        if not os.access(destination_dir, os.W_OK):
            print(f"No write permission in {destination_dir}")
            return False
            
        # Copy the file
        shutil.copy2(source_file, destination_dir)
        print("File copied successfully")
        return True
        
    except PermissionError:
        print("Permission denied")
        return False
    except shutil.SameFileError:
        print("Source and destination are the same file")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def stream_data(text:str):
   print(f"stream_data: {text}")
   for word in text.split(" "):
      yield word + " "
      time.sleep(0.01)