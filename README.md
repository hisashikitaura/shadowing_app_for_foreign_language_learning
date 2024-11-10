# MY PROJECT: Shadowing For English Language Learner

In shadowing practice, a teacher (or AI bot) reads the foreign language sentence by sentence aloud, and learners(= you) repeat at the same pace, with a slight delay if possible.
You do shadowing practice with a favorite topic because the AI bot makes sentences for shadowing as you like.
So you specifies a desired topic, number of sentences, and your skill level.  

This application was created for the NVIDIA Developer Contest (2024).
Please enjoy it and don't hesitate to ask me anything.

## Features

- User-friendly GUI interface for topic selection
- Customizable input text for targeted content generation
- Content appropriateness checker for educational purposes
- AI-powered text generation optimized for your skill level
- Text-to-speech bot that reads generated sentences sequentially

## Technologies Used

- NVIDIA NeMo GuardRails
* [NVIDIA NeMo GuardRails](https://docs.nvidia.com/nemo/guardrails/introduction.html)
- NVIDIA NIM (meta/llama-3.1-405b-instruct)
* [NVIDIA NIM (meta/llama-3.1-405b-instruct)](https://build.nvidia.com/meta/llama-3_1-405b-instruct)
- NVIDIA NIM (nvidia/fastpitch-hifigan-tts)
* [NVIDIA NIM (nvidia/fastpitch-hifigan-tts)](https://build.nvidia.com/nvidia/fastpitch-hifigan-tts)
- LlamaIndex (Faiss Vector Store)
* [LlamaIndex (Faiss Vector Store)](https://docs.llamaindex.ai/en/stable/examples/vector_stores/FaissIndexDemo/)
- NVIDIA NIM (nvidia/nv-embedqa-mistral-7b-v2) * as a custom embedding provider within LlamaIndex
* [NVIDIA NIM (nvidia/nv-embedqa-mistral-7b-v2)](https://build.nvidia.com/nvidia/nv-embedqa-mistral-7b-v2)
- Streamlit

## Requirements

1. Python 3.8+
2. C++ Runtime (for NVIDIA GuardRails) 
3. NVIDIA GPU (for NVIDIA text-to-speech service)

## Installation

1. Clone this repository
2. Create virtual environment `python -m venv .venv`
3. Install C++ Runtime
* [Installation Guide](https://docs.nvidia.com/nemo/guardrails/getting_started/installation-guide.html)
- [Install the Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
4. Install NVIDIA Riva clients
* [Install NVIDIA Riva clients](https://github.com/nvidia-riva/python-clients/tree/main)
- Clone ``riva-python-clients`` repo and change to the repo root
- Run commands
```bash
git clone https://github.com/nvidia-riva/python-clients.git
cd python-clients
git submodule init
git submodule update --remote --recursive
pip install -r requirements.txt
python3 setup.py bdist_wheel
pip install --force-reinstall dist/*.whl
```
5. Install requirements `pip install -r requirements.txt`
6. Set your OPENAI_API_KEY and NVIDIA_API_KEY in the .env file.
7. Check the volume of your computer speakers.
8. Run the application `streamlit run streamlit_app.py`

## Project Structure

shadowing_app_for_foreign_language_learning/
├──config/    # GuardRails files
|    └─rails/ 
├──image/     # logo file
├──llms/      # api files
├──prompts/   # prompt files
|    └─templates/ 
├──python-clients/ # NVIDIA Riva Python clients files
├──sample_voice/ # sample files
├──services/   # shadowing and tts
├──store/      # generated text and voice files(.wav)
└──utils/      # library files
