class Config:
    # LLM Mode
    GPT_4O_MINI = "gpt-4o-mini"
    OPENAI_GPT_4O_MINI = "OpenAI/gpt-4o-mini"
    META_LLAMA_3_2_3b_INSTRUCT = "meta/llama-3.2-3b-instruct"
    NVIDIA_NIM_META_LLAMA_3_2_3B_INSTRUCT = "NVIDIA NIM/meta/llama-3.2-3b-instruct"
    NVIDIA_NIM_NVIDIA_EMBEDQA_e5_v5 = "nvidia/nv-embedqa-e5-v5"
    NVIDIA_NIM_LLAMA_3_2_NV_EMBEDQA_1B_V1 = "llama-3.2-nv-embedqa-1b-v1"
    NVIDIA_NIM_NV_EMBEDQA_MISTRAL_7B_V2 = "nvidia/nv-embedqa-mistral-7b-v2"
    NVIDIA_NIM_GUARDRAILS = "NVIDIA Guardrails"

    # NVIDIA_TextToSpeech_VOICE
    VOICE_ENG_FEMALE_1 = "English-US.Female-1"
    VOICE_ENG_MALE_1 = "English-US.Male-1"
    VOICE_ENG_FEMALE_NEUTRAL = "English-US.Female-Neutral"
    VOICE_ENG_MALE_NEUTRAL = "English-US.Male-Neutral"
    VOICE_ENG_FEMALE_ANGRY = "English-US.Female-Angry"
    VOICE_ENG_MALE_ANGRY = "English-US.Male-Angry"
    VOICE_ENG_FEMALE_CALM = "English-US.Female-Calm"
    VOICE_ENG_MALE_CALM = "English-US.Male-Calm"
    VOICE_ENG_FEMALE_HAPPY = "English-US.Female-Happy"
    VOICE_ENG_MALE_HAPPY = "English-US.Male-Happy"

    # OTHER
    SAMPLE_VOICE = "sample_voice"
    AUDIO_MPEG = "audio/mpeg"
    USER_PREFERENCE_FILE = "user_preferences.txt"
    NEW_LINE = "\r\n"   # Windows
    UTF_8 = "utf-8"