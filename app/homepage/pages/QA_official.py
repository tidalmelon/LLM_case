import streamlit as st
from streamlit_chatbox import ChatBox, FakeLLM, Markdown
import time



#class FakeLLM:
#    def _answer(self, query: str) -> str:
#        answer = f" \n\n{query}"  # 这里什么都不写
#        docs = ["reference 1", "reference 2", "reference 3"]
#        return answer, docs
#
#    def chat(self, query: str) -> str:
#        return self._answer(query)
#
#    def chat_stream(self, query: str):
#        text, docs = self._answer(query)
#        for t in text:
#            yield t, docs
#            time.sleep(0.1)



llm = FakeLLM()
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
    if streaming:
        generator = llm.chat_stream(query)
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

        time.sleep(1)

        text = ""

        for x, docs in generator:
            text += x
            chat_box.update_msg(text, element_index=0, streaming=True)

        # update the element without focus
        chat_box.update_msg(text, element_index=0, streaming=False, state="complete")
    else:
        text, docs = llm.chat(query)
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                         expanded=True, title="answer"),
                Markdown("\n\n".join(docs), in_expander=in_expander,
                         title="references"),
            ]
        )




