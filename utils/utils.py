import streamlit as st

import time

@st.dialog("😏Your favorite text??😏")
def show_text(text) -> bool:
  """
  This shows modal dialog with the generated text.
  And a user has to choose one.
  st.dialog function can't return a value.
  """
  st.html(text)

  if st.button("OK", key=0):
    st.balloons()
    time.sleep(2)
    st.success("😍Fantastic!!😍", icon="😍")
    st.session_state.flag["create_voice_flag"] = True
    print("OK_create_voice_flag: ", st.session_state.flag["create_voice_flag"])    
    st.rerun()
  if st.button("Cancel", key=1):
    st.info("😌Don't go away and let's practice!😌", icon="😌")
    st.session_state.flag["create_voice_flag"] = False
    print("Cancel_create_voice_flag: ", st.session_state.flag["create_voice_flag"])        
    st.rerun()