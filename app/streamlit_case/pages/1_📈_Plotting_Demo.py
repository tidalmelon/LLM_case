import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="绘图演示", page_icon="📈")

st.markdown("# 绘图演示")
st.sidebar.header("绘图演示")
st.write(
    """这个演示展示了 Streamlit 的绘图和动画组合。我们在一个循环中生成一些随机数大约5秒钟。希望你喜欢！"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
# 构建动画折线图, 可以用于写监控?
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("完成%i%%" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit 的部件会自动按顺序运行脚本。由于此按钮与任何其他逻辑都没有连接，因此它只会引起简单的重新运行。
st.button("重新运行")
