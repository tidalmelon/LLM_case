import streamlit as st


if st.session_state['authentication_status']:

    if "PINECONE_API_KEY" not in  st.session_state:
        st.session_state['PINECONE_API_KEY'] = ""
    
    if "PINECONE_ENVIRONMENT" not in  st.session_state:
        st.session_state['PINECONE_ENVIRONMENT'] = ""
    
    
    st.set_page_config(page_title="Pinecone Setting", layout="wide")
    
    st.title("Pinecone Settings")
    
    pinecone_api_key = st.text_input("pinecone_api_key", value=st.session_state["PINECONE_API_KEY"], max_chars=None, key=None, type="default") # default 
    pinecone_environment = st.text_input("pinecone_environment", value=st.session_state["PINECONE_ENVIRONMENT"], max_chars=None, key=None, type="default") # default 
    
    
    saved = st.button("Save")
    
    if saved:
        st.session_state['PINECONE_API_KEY'] = pinecone_api_key
        st.session_state['PINECONE_ENVIRONMENT'] = pinecone_environment


