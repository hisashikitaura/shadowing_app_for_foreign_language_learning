#%%
import openai

from llama_index.core import PromptTemplate
from llms.utils import use_nvidia_guardrails
from nemoguardrails import RailsConfig, LLMRails

import os
from pathlib import Path
from dotenv import load_dotenv

from prompts.system_prompt import SYSTEM_PROMPT
from prompts.templates.user_template import USER_TEMPLATE



# model
NVIDIA_NIM_GUARDRAILS = "NVIDIA Guardrails"

model = NVIDIA_NIM_GUARDRAILS

load_dotenv()
openai_api_key = str(os.getenv("OPENAI_API_KEY"))

#%%
config = RailsConfig.from_path("./config")
rails = LLMRails(config)

# user_prompt = PromptTemplate(USER_TEMPLATE).format(language_name="English", topic="Michael Jackson", num_sentences=10, level="Proficiency")
# messages = [
#             {"role": "user", "content": user_prompt}    # system prompt is not needed because it is already included in the NemoGuardrails' config.yml
#         ]
response_topic_detail = "Jackson sang from childhood, and over time his voice and vocal style changed. Between 1971 and 1975, his voice descended from boy soprano to lyric tenor.[461] He was known for his vocal range.[426] With the arrival of Off the Wall in the late 1970s, Jackson's abilities as a vocalist were well regarded; Rolling Stone compared his vocals to the \"breathless, dreamy stutter\" of Stevie Wonder, and wrote that \"Jackson's feathery-timbred tenor is extraordinarily beautiful."
user_prompt = PromptTemplate(USER_TEMPLATE).format(language_name="English", topic="Michael Jackson", content={response_topic_detail}, num_sentences=10, level="Advanced")
messages = [
    # {
    # "role": "context",
    # "content": {"relevant_chunks": """
    #     Michael Jackson's vocal style: Jackson sang from childhood, and over time his voice and vocal style changed. Between 1971 and 1975, his voice descended from boy soprano to lyric tenor.[461] He was known for his vocal range.[426] With the arrival of Off the Wall in the late 1970s, Jackson's abilities as a vocalist were well regarded; Rolling Stone compared his vocals to the \"breathless, dreamy stutter\" of Stevie Wonder, and wrote that \"Jackson's feathery-timbred tenor is extraordinarily beautiful.
    # """}
    # },
    {
    "role": "user",
    "content": user_prompt
    }
]
response = rails.generate(messages=messages)

#%%
print(response['content'])

#**************************************
#%%
info = rails.explain()

#%%
info.print_llm_calls_summary()

#%%
print(info.llm_calls[0].prompt)

# %%
print(info.llm_calls[0].completion)

# %%
print(info.llm_calls[1].prompt)
# %%
print(info.llm_calls[1].completion)

#%%
print(response)

# %%
print(info.colang_history)
# %%
