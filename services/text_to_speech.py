import subprocess
import re
from dotenv import load_dotenv

import streamlit as st
import openai

from llms.utils import check_openai_api_key, check_nvidia_api_key
from utils.utils import create_path, copy_multiple_files
from config import Config

load_dotenv()


def create_voice_file(text:str, path:str, uuid:str, teacher:str="👩‍🦰", emotion:str="😐") -> None:
  """
  Create speech with TTS model.
  This function is for one sentence.
  """
  print("Creating voice file...")
  print(f"no1. text: {text}, path: {path}, uuid: {uuid}, teacher: {teacher}, emotion: {emotion}")
  # split the text into sentences
  sentences = []
  sentences = re.findall('<p>(.*?)</p>', text)
  
  file_save_path = create_path(path, uuid)
  file_list = []

  voice = select_voice(teacher, emotion)
  for i, s in enumerate(sentences):
    resonse = run_nvidia_fastpitch_hifigan_tts(s, i, voice)
    file_name = f"{i}.wav"
    file_list.append(file_name)
  copy_multiple_files(file_list, file_save_path)


def select_voice(teacher:str, emotion:str) -> str:
  """
  Select a voice for the text to speech.
  """
  if teacher == "👩‍🦰":
    if emotion == "😐":
      return Config.VOICE_ENG_FEMALE_1
    elif emotion == "🥰":
      return Config.VOICE_ENG_FEMALE_HAPPY
    elif emotion == "😴":
      return Config.VOICE_ENG_FEMALE_CALM
    elif emotion == "😡":
      return Config.VOICE_ENG_FEMALE_ANGRY
    elif emotion == "😑":
      return Config.VOICE_ENG_FEMALE_NEUTRAL
    else:
      print("Error: 👩‍🦰 emotion is not found.")
      return None
  elif teacher == "👨‍🦰":
    if emotion == "😐":
      return Config.VOICE_ENG_FEMALE_1
    elif emotion == "🥰":
      return Config.VOICE_ENG_FEMALE_HAPPY
    elif emotion == "😴":
      return Config.VOICE_ENG_FEMALE_CALM
    elif emotion == "😡":
      return Config.VOICE_ENG_FEMALE_ANGRY
    elif emotion == "😑":
      return Config.VOICE_ENG_FEMALE_NEUTRAL
    else:
      print("Error: 👨‍🦰 emotion is not found.")
      return None
  else:
    print("Error: teacher is not found.")
    print("To be continued(teacher=👩‍🦰, emotion=😐)")
    return Config.VOICE_ENG_FEMALE_1


def run_openai_tts(text: str, file_save_path: str, i: int) -> bool:
    """
    https://platform.openai.com/docs/guides/text-to-speech/
    """
    openai_api_key = check_openai_api_key()
    with openai.audio.speech.with_streaming_response.create(
      model="tts-1",
      voice="nova", #'nova', 'shimmer', 'echo', 'onyx', 'fable' or 'alloy'
      input=text,
      speed=1,
    ) as response:
      try:
        response.stream_to_file(f"{file_save_path}/{i}.wav")
      except Exception as e:
        st.error(e, "😩")


def run_nvidia_fastpitch_hifigan_tts(text: str, i: int, voice:str) -> bool:
    """
    https://build.nvidia.com/nvidia/fastpitch-hifigan-tts/api
    Available voices:
            "English-US.Female-1",
            "English-US.Male-1",
            "English-US.Female-Neutral",
            "English-US.Male-Neutral",
            "English-US.Female-Angry",
            "English-US.Male-Angry",
            "English-US.Female-Calm",
            "English-US.Male-Calm",
            "English-US.Female-Fearful",
            "English-US.Female-Happy",
            "English-US.Male-Happy",
            "English-US.Female-Sad"
    """
    print(f"no2. text: {text}, i: {i}, voice: {voice}")
    nvidia_api_key = check_nvidia_api_key()

    # Define the command as a list of arguments
    # Output file can only be in the current working directory 
    command = ["python", "python-clients/scripts/tts/talk.py",\
                "--server", "grpc.nvcf.nvidia.com:443",\
                "--use-ssl",\
                "--metadata", "function-id", "0149dedb-2be8-4195-b9a0-e57e0e14f972",\
                "--metadata", "authorization", f"Bearer {nvidia_api_key}",\
                "--text", text,\
                "--voice", voice,\
                # "--output", f"{file_save_path}/{i}.wav"]
                "--output", f"{i}.wav"]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
      print("Script ran successfully")
      print("Output:", result.stdout)
      return True
    else:
      print("Script failed")
      print("Error:", result.stderr)
      return False