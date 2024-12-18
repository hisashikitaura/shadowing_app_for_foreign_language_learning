from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI as OpenAILlamaIndex
from llama_index.core import PromptTemplate, SummaryIndex, VectorStoreIndex, load_index_from_storage, StorageContext, Settings, Document
from llama_index.readers.web import SimpleWebPageReader, SpiderWebReader
from llama_index.core.node_parser.text import TokenTextSplitter, SentenceSplitter
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from openai import OpenAI as OpenAIOriginal
import streamlit as st
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss

from nemoguardrails import RailsConfig, LLMRails

import os
import nest_asyncio

from prompts.system_prompt import SYSTEM_PROMPT
from prompts.templates.user_template import USER_TEMPLATE_CREATE, USER_TEMPLATE_EXTRACT
from config import Config

nest_asyncio.apply()

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

def check_spider_api_key():
    spider_api_key = os.environ["SPIDER_API_KEY"]
    assert spider_api_key.startswith(
        "sk-"
    ), f"{spider_api_key[:5]}... is not a valid key"
    return spider_api_key


def create_text(language_name="English", topic="Foods", topic_url=None, num_sentences=5, level="Beginner", model=Config.NVIDIA_NIM_GUARDRAILS) -> str:
  """
  Create text for shadowing practice.
  """
  if model == Config.OPENAI_GPT_4O_MINI:  #deprecated
    # text = use_openai_gpt_4o_mini(language_name, topic, num_sentences, level)
    pass
  elif model == Config.NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT: #deprecated
    # text = use_nvidia_nim_meta_llama_3_2_3b_instruct(language_name, topic, num_sentences, level)
    pass
  elif model == Config.NVIDIA_NIM_GUARDRAILS:
    text = use_nvidia_guardrails(language_name, topic, topic_url, num_sentences, level)    
  else:
    st.error("😩Please select a model.😩", "😩")

  return text


# def use_openai_gpt_4o_mini(language_name, topic, num_sentences, level, openai_api_key):
#     """
#     Use OpenAI's GPT-4o-mini model.
#     """
#     openai_api_key = check_openai_api_key()

#     ASSISTANT = "assistant:"
#     llm = ChatMessage(model=Config.GPT_4O_MINI,
#                     temperature=0.8,
#                     max_tokens=None,
#                     timeout=None,
#                     max_retries=2,
#                     openai_api_key=openai_api_key)
    
#     user_prompt = PromptTemplate(USER_TEMPLATE_GENERATE).format(language_name=language_name, topic=topic, relevant_chunks=None, num_sentences=num_sentences, level=level)
#     messages = [
#                 ChatMessage(role="system", content=SYSTEM_PROMPT),
#                 ChatMessage(role="user", content=user_prompt)
#             ]
    
#     res_text = OpenAILlamaIndex().chat(messages)
#     return str(res_text).replace(ASSISTANT, "").strip()


# def use_nvidia_nim_meta_llama_3_2_3b_instruct(language_name, topic, num_sentences, level):
#     """
#     Use NVIDIA NIM's meta/llama-3.2-3b-instruct model.
#     """
#     nvidia_api_key = check_nvidia_api_key()

#     client = OpenAIOriginal(
#         base_url = "https://integrate.api.nvidia.com/v1",
#         api_key = nvidia_api_key
#     )   

#     user_prompt = PromptTemplate(USER_TEMPLATE_GENERATE).format(language_name=language_name, topic=topic, content=None, num_sentences=num_sentences, level=level)
#     messages = [
#                 ChatMessage(role="system", content=SYSTEM_PROMPT),
#                 ChatMessage(role="user", content=user_prompt)
#             ]

#     completion = client.chat.completions.create(
#         model=Config.META_LLAMA_3_2_3b_INSTRUCT,
#         messages=messages,
#         temperature=0.8,
#         top_p=0.7,
#         max_tokens=None,
#     )

#     text = completion.choices[0].message.content
#     return text


def use_nvidia_guardrails(language_name, topic, topic_url, num_sentences, level):
    """
    Use NVIDIA's guardrails.
    At this time, the model is llama-3.2-3b-instruct fixed.
    """
    config = RailsConfig.from_path("./config")
    rails = LLMRails(config)

    if topic_url is None:
      user_prompt = PromptTemplate(USER_TEMPLATE_CREATE).format(language_name=language_name, topic=topic, relevant_chunks=None, num_sentences=num_sentences, level=level)
      messages = [{
            "role": "user",   # system prompt is not needed because it is already included in the NemoGuardrails' config.yml
            "content": user_prompt
      }]
    elif topic_url is not None:
      # Error: "Input length 1232 exceeds maximum allowed token size 512"
      Settings.embed_model = set_nvidia_embedder()
      Settings.chunk_size = set_nvidia_embedder_dimention()

      documents = SimpleWebPageReader(html_to_text=True).load_data([topic_url])
      sentenceSplitter = SentenceSplitter().from_defaults(chunk_size=300, chunk_overlap=50, separator=" ")
      texts = sentenceSplitter.split_text(documents[0].text)
      print(f"len(texts): {len(texts)}")
      documents = [Document(text=t) for t in texts]

      # create a faiss index
      d = 4096  # dimension depending on the model
      faiss_index = faiss.IndexFlatL2(d)
      # print(f"VectorStoreInded: start")
      vector_store = FaissVectorStore(faiss_index=faiss_index)
      storage_context = StorageContext.from_defaults(vector_store=vector_store)
      index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
      # print(f"VectorStoreInded: end")

      query_engine = index.as_query_engine()
      relevant_chunks = query_engine.query(PromptTemplate(USER_TEMPLATE_EXTRACT).format(topic=topic))
      print(f"relevant_chunks: {relevant_chunks}")

      user_prompt = PromptTemplate(USER_TEMPLATE_CREATE).format(language_name=language_name, topic=topic, relevant_chunks=str(relevant_chunks), num_sentences=num_sentences, level=level)
      print(f"user_prompt: {user_prompt}")
      messages = ([
          {
            "role": "user",
            "content": user_prompt
          }
      ])
    response = rails.generate(messages=messages)
    info = rails.explain()
    print(f"generate response: {response['content']}")
    return response['content']


def set_nvidia_embedder():
  # https://build.nvidia.com/nvidia/nv-embedqa-e5-v5/modelcard
  return NVIDIAEmbedding(model=Config.NVIDIA_NIM_NV_EMBEDQA_MISTRAL_7B_V2)

def set_nvidia_embedder_dimention():
  return 512