import streamlit as st

st.set_page_config(
    page_title="你好",
    page_icon="👋",
)

st.write("# 欢迎使用 Streamlit! 👋")

# 侧边栏
st.sidebar.success("在上方选择一个演示。")

st.markdown(
    """
    Streamlit 是一个专为机器学习和数据科学项目而构建的开源应用框架。
    **👈 从侧边栏选择一个演示**，看看 Streamlit 能做什么吧！
    ### 想了解更多吗？
    - 查看 [streamlit.io](https://streamlit.io)
    - 阅读我们的 [文档](https://docs.streamlit.io)
    - 在我们的 [社区论坛](https://discuss.streamlit.io) 提问
    ### 查看更复杂的示例
    - 使用神经网络来 [分析 Udacity 自动驾驶汽车图像数据集](https://github.com/streamlit/demo-self-driving)
    - 探索一个 [纽约市乘车数据集](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

