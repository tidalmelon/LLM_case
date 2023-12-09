import streamlit as st
import pandas as pd
import numpy as np
import random


st.header("请直接看这里把, 太多了: https://blog.csdn.net/weixin_46043195/article/details/132164653")


st.subheader("1. 你甚至可以使用 Pandas Styler 对象来改变呈现的数据框的样式。这是不是很酷？")


df = pd.DataFrame(
   np.random.randn(10, 20),
   columns=('col %d' % i for i in range(20)))

st.dataframe(df.style.highlight_max(axis=0))


st.subheader("2. 通过将 st.dataframe 与 Pandas Styler 结合使用，你可以轻松地打造出具有个性化视觉效果的数据展示")


df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)










































