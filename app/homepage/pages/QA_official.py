import streamlit as st
from streamlit_chatbox import ChatBox, Markdown

from transformers import AutoModel, AutoTokenizer





@st.cache_resource
def load_llm():
    path = '/root/.cache/huggingface/hub/THUDM/chatglm2-6b-32k'
    tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    llm = AutoModel.from_pretrained(path, trust_remote_code=True).quantize(8).half().cuda()
    return tokenizer, llm


tokenizer, llm = load_llm()

chat_box  = ChatBox()

# 官网给出根据column可以放置到右边. 可以参考chatchat
with st.sidebar:
    st.subheader("Start to chat using streamlit")
    streaming = st.checkbox("streaming", True)
    in_expander = st.checkbox("show messages in expander", True)
    show_history = st.checkbox("show history", False)



chat_box.init_session()
chat_box.output_messages()

if query := st.chat_input('input your question here'):
    chat_box.user_say(query)
    #if streaming:
    if True:
        # history is setted to []
        generator = llm.stream_chat(tokenizer, 
                                    query, 
                                    history=[],
                                    max_length=10000,
                                    temperature=0.01,
                                    top_p=0.4,
                                    top_k=10)
        elements = chat_box.ai_say(
                [
                    Markdown("", 
                             expanded=True, 
                             #in_expander=in_expander, # 是否显示转圈
                             #title="answer"
                             ),
                    #Markdown("", in_expander=in_expander, title="references"),
                ]
        )

        for text, history in generator:
            chat_box.update_msg(text, element_index=0, streaming=True)

        # update the element without focus
        chat_box.update_msg(text, element_index=0, streaming=False, state="complete")




