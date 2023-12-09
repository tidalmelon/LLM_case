import streamlit as st
import numpy as np



st.header("1. st.columns: 并排布局多元素容器")


st.markdown("* 您可以将多个容器放置在主要内容区域内\n * 能将多元素容器嵌套在其他多元素容器内")


col1, col2, col3 = st.columns(3)


with col1:
   st.header("一只猫")
   st.image("https://static.streamlit.io/examples/cat.jpg")


with col2:
   st.header("一只狗")
   st.image("https://static.streamlit.io/examples/dog.jpg")


with col3:
   st.header("一只猫头鹰")
   st.image("https://static.streamlit.io/examples/owl.jpg")




col1, col2 = st.columns([3, 1])
data = np.random.randn(10, 1)

col1.subheader("一个宽容器，含有图表")
col1.line_chart(data)

col2.subheader("一个窄容器，含有数据")
col2.write(data)




st.header("2. st.tabs: 以选项卡形式布局多元素容器")

st.markdown("选项卡注意事项: 每个选项卡的所有内容都会被一次性发送并渲染在前端，目前不支持条件渲染。这意味着无论用户是否查看某个选项卡，所有内容都会被加载和渲染。在设计应用时，请确保选项卡内的内容在逻辑上是相关的，避免出现不必要的数据传输和渲染。")

tab1, tab2, tab3 = st.tabs(["猫", "狗", "猫头鹰"])

with tab1:
   st.header("一只猫")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("一只狗")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("一只猫头鹰")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



tab1, tab2 = st.tabs(["📈 图表", "🗃 数据"])
data = np.random.randn(10, 1)

tab1.subheader("一个带有图表的选项卡")
tab1.line_chart(data)

tab2.subheader("一个带有数据的选项卡")
tab2.write(data)




st.header("3. st.expander - 可展开/折叠的多元素容器")

st.markdown("st.expander 注意事项: \n st.expander 嵌套在另一个 st.expander 内。如果需要多层次的展开/折叠功能，您可以使用其他布局组件进行组合。")

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("查看说明"):
    st.write("""
        上面的图表展示了我为您选择的一些数字。
        这些数字是通过真实的骰子摇出来的，所以它们*保证*是随机的。
    """)
    st.image("https://static.streamlit.io/examples/dice.jpg")





st.header("4. std.container - 插入多元素容器")
with st.container():
   st.write("这是容器内的内容: 您可以调用任何 Streamlit 命令，包括自定义组件：")

   st.bar_chart(np.random.randn(50, 3))

st.write("这是容器外的内容")



st.header("5. st.empty - 插入单元素容器")


st.markdown("这为您提供了更多的灵活性，您可以根据应用的需求，动态地展示不同的内容。通过 st.empty 插入的元素可以在任何时候进行替换或清除操作")

st.markdown("下面的容器之所以看不见,是因为是单元素容器")


placeholder = st.empty()

# 用一些文本替换占位符：
placeholder.text("你好")

# 用一个图表替换文本：
placeholder.line_chart({"data": [1, 5, 2, 6]})

# 用多个元素替换图表：
with placeholder.container():
    st.write("这是一个元素")
    st.write("这是另一个元素")

# 清除所有这些元素：
placeholder.empty()
























