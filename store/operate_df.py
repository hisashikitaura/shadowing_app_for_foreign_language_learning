import streamlit as st

import pandas as pd
from pathlib import Path
from config import Config

csv_path = Path("__file__").parent / "store"

def create_df(csv_path:str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def create_st_dataframe(csv_path:str) -> st.Dataframe:
    st.dataframe(create_df(csv_path))

def show_user_preferences(csv_path:str) -> None:
    create_st_dataframe(csv_path)

def show_text(csv_path:str, uuid:str) -> None:
    create_st_dataframe(csv_path)