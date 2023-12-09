import streamlit as st
import time


st.subheader("语法方式:")

st.code("""
# 使用对象表示法
st.sidebar.[element_name]

# "with" 语法
with st.sidebar:
    st.[element_name]
        """)


# 使用对象表示法添加选择框
add_selectbox = st.sidebar.selectbox(
    "您希望如何联系您？",
    ("电子邮件", "家庭电话", "移动电话")
)


# 使用“with”语法添加单选按钮
with st.sidebar:
    add_radio = st.radio(
        "选择一种运输方式",
        ("标准（5-15天）", "快递（2-5天）")
    )

    with st.echo():
        st.write("这段代码将在侧边栏中显示。")

    with st.spinner("加载中..."):
        time.sleep(5)
    st.success("完成！")
