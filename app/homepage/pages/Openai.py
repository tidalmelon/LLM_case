import streamlit as st


if st.session_state['authentication_status']:


    if "OPEN_AI_KEY" not in  st.session_state:
        st.session_state['OPEN_AI_KEY'] = ""
    
    
    st.set_page_config(page_title="OpenAI Setting", layout="wide")  # header title
    
    st.title("OpenAI Settings") # H1 title
    
    open_ai_key = st.text_input("API Key", value=st.session_state["OPEN_AI_KEY"], max_chars=None, key=None, type="default") # default 
    
    
    saved = st.button("Save")
    
    if saved:
        st.session_state['OPEN_AI_KEY'] = open_ai_key


