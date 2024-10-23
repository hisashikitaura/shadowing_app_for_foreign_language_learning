import subprocess
import openai

import streamlit as st

from dotenv import load_dotenv

from llms.utils import check_openai_api_key, check_nvidia_api_key

load_dotenv()



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
        response.stream_to_file(f"{file_save_path}/{i}.mp3")
      except Exception as e:
        st.error(e, "😩")


def run_nvidia_fastpitch_hifigan_tts(text: str, file_save_path: str, i: int) -> bool:
    """
    https://build.nvidia.com/nvidia/fastpitch-hifigan-tts/api
    """
    nvidia_api_key = check_nvidia_api_key()
    NVIDIA_TTS_VOICE = 'English-US.Female-1'

    # Define the command as a list of arguments
    # Output file can only be in the current working directory 
    command = ["python", "python-clients/scripts/tts/talk.py",\
                "--server", "grpc.nvcf.nvidia.com:443",\
                "--use-ssl",\
                "--metadata", "function-id", "0149dedb-2be8-4195-b9a0-e57e0e14f972",\
                "--metadata", "authorization", f"Bearer {nvidia_api_key}",\
                "--text", text,\
                "--voice", NVIDIA_TTS_VOICE,\
                # "--output", f"{file_save_path}/{i}.wav"]
                "--output", f"{i}.mp3"]

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