import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Welcome to ASL", layout="wide")
    
st.title("Welcome to ASL")

def main():
    if "PINECONE_API_KEY" not in  st.session_state:
        st.session_state['PINECONE_API_KEY'] = ""
        
    if "PINECONE_ENVIRONMENT" not in  st.session_state:
        st.session_state['PINECONE_ENVIRONMENT'] = ""
        
        
    if "OPEN_AI_KEY" not in  st.session_state:
        st.session_state['OPEN_AI_KEY'] = ""

    
    with st.container():
        st.header("OpenAI Settings")
        st.markdown(f"""
        |keys|values|
        |---|---|
        |OPEN_AI_KEY| {st.session_state['OPEN_AI_KEY']}|
        """)
    
    
    with st.container():
        st.header("PineCone Settings")
        st.markdown(f"""
        |keys|values|
        |---|---|
        |PINECONE_API_KEY| {st.session_state['PINECONE_API_KEY']}|
        |PINECONE_ENVIRONMENT| {st.session_state['PINECONE_ENVIRONMENT']}|
        """)



if __name__ == '__main__':

    names = ['admin'] # 用户名
    usernames = ['admin', '']  # 登录名
    passwords = ['123456']

    hashed_passwords = stauth.Hasher(passwords).generate()


	# 定义字典，初始化字典
    credentials = {'usernames': {}}
    # 生成服务器端的用户身份凭证信息
    for i in range(0, len(names)):
        credentials['usernames'][usernames[i]] = {'name': names[i], 'password': hashed_passwords[i]}
    authenticator = stauth.Authenticate(credentials, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=0)
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:  # 登录成功
        main()
    elif authentication_status == False:  #登录失败
        st.error('Username/password is incorrect')
    elif authentication_status == None:  #未输入登录信息
        st.warning('Please enter your username and password')
































