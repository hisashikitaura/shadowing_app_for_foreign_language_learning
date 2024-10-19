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

user_prompt = PromptTemplate(USER_TEMPLATE).format(language_name="English", topic="Noguchi Hideyo", num_sentences=10, level="Beginner")
messages = [
            {"role": "user", "content": user_prompt}    # system prompt is not needed because it is already included in the NemoGuardrails' config.yml
        ]
response = rails.generate(messages=messages)

#%%
print(response['content'])

#**************************************
#%%
info = rails.explain()

#%%
info.print_llm_calls_summary()


 
# %%
print(info.llm_calls[1].prompt)
# %%
print(info.llm_calls[1].completion)

#%%
print(response)

# %%
print(info.colang_history)
# %%
