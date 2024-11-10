import os
import csv

from utils.utils import remove_ptag
from config import Config


def store_text(text:str, file_save_path:str, uuid:str):
  """
  Store the generated text in a flat file.
  This text includs <p> and </p> tags, therefore it is necessary to remove them.
  """
  print("Storing text...")
  with open(f"{file_save_path}/{uuid}/{uuid}.txt", "w", encoding=Config.UTF_8) as f:
    f.write(text)


def store_user_preference(text:str, file_save_path:str, uuid:str, topic:str, level:str, teacher:str, emotion:str) -> None:
  """
  Store the user prefereces in a flat file.
  This text includs <p> and </p> tags, therefore it is necessary to remove them.
  """
  print("Storing user preferences...")
  first_sentence = remove_ptag(text, False).split(Config.NEW_LINE)[0]

  recored_list = [uuid, topic, level, teacher, emotion, first_sentence]
  if not os.path.isfile(f"{file_save_path}/{Config.USER_PREFERENCE_FILE}"):
    with open(f"{file_save_path}/{Config.USER_PREFERENCE_FILE}", "w", encoding=Config.UTF_8) as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(recored_list)
  else:
    with open(f"{file_save_path}/{Config.USER_PREFERENCE_FILE}", "a", encoding=Config.UTF_8) as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(recored_list)


