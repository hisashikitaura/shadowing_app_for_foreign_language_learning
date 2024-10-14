from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI as OpenAILlamaIndex
from llama_index.core import PromptTemplate

# https://docs.llamaindex.ai/en/stable/examples/embeddings/nvidia/
from llama_index.embeddings.nvidia import NVIDIAEmbedding

from openai import OpenAI as OpenAIOriginal

import getpass
import os
import json

from prompts.template import TEMPLATE

# model
OPENAI_GPT_4O_MINI = "OpenAI/gpt-4o-mini"
NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT = "NVIDIA NIM/meta/llama-3.2-3b-instruct"


def check_openai_api_key():
    openai_api_key = os.environ["OPENAI_API_KEY"]
    assert openai_api_key.startswith(
        "sk-"
    ), f"{openai_api_key[:5]}... is not a valid key"
    return openai_api_key



def check_nvidia_api_key():
    nvapi_key = os.environ["NVIDIA_API_KEY"]
    assert nvapi_key.startswith(
        "nvapi-"
    ), f"{nvapi_key[:5]}... is not a valid key"
    return nvapi_key


def use_openai_gpt_4o_mini(language_name, topic, num_sentences, level, openai_api_key):
    """
    Use OpenAI's GPT-4o-mini model.
    """
    openai_api_key = check_openai_api_key()

    ASSISTANT = "assistant:"
    llm = ChatMessage(model='gpt-4o-mini',
                    temperature=0.8,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                    openai_api_key=openai_api_key)

    qa_template = PromptTemplate(TEMPLATE)
    prompt = qa_template.format(language_name=language_name, topic=topic, num_sentences=num_sentences, level=level)
    messages = [
                ChatMessage(role="system", content="You're a text generator that a user wants. No talks."),
                ChatMessage(role="user", content=prompt)
            ]
    
    res_text = OpenAILlamaIndex().chat(messages)
    return str(res_text).replace(ASSISTANT, "").strip()


def use_nvidia_nim_meta_llama_3_2_3b_instruct(language_name, topic, num_sentences, level):
    """
    Use NVIDIA NIM's meta/llama-3.2-3b-instruct model.
    """
    nvidia_api_key = check_nvidia_api_key()

    client = OpenAIOriginal(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = nvidia_api_key
    )   

    qa_template = PromptTemplate(TEMPLATE)
    prompt = qa_template.format(language_name=language_name, topic=topic, num_sentences=num_sentences, level=level)
    messages = [
                ChatMessage(role="system", content="You're a text generator that a user wants. No talks."),
                ChatMessage(role="user", content=prompt)
            ]

    completion = client.chat.completions.create(
        model="meta/llama-3.2-3b-instruct",
        messages=messages,
        temperature=0.8,
        top_p=0.7,
        max_tokens=None,
    )

    text = completion.choices[0].message.content
    print(text)
    return text