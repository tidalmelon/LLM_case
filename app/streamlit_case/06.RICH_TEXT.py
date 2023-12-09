import streamlit as st
import pandas as pd
import numpy as np




st.subheader('1. st.markdown - 引入丰富的Markdown文本')

st.markdown('Streamlit is **_really_ cool**.')
st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")

st.subheader('2. st.title - 引入引人注目的大标题: 颜色,自定义表情')

st.title('This is a title')
st.title('A title with _italics_ :blue[colors] and emojis :sunglasses:')


st.subheader('3. st.header - 引入简洁的小标题')
st.header('This is a header')
st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')


st.subheader('4. st.subheader - 添加次级标题')

st.subheader('This is a subheader')
st.subheader('A subheader with _italics_ :blue[colors] and emojis :sunglasses:')



st.subheader('5. st.caption - 添加解释性文字')

st.caption('This is a string that explains something above.')
st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')



st.subheader('6. st.code - 显示代码块')
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')


st.subheader('7.st.text - 显示文本')

st.text('This is some text.')


st.subheader('8. st.latex - 显示LaTeX公式')

st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')


st.subheader('9. st.divider - 添加分隔线')

st.write("This is some text.")
st.slider("This is a slider", 0, 100, (25, 75))
st.divider()  # Draws a horizontal rule
st.write("This text is between the horizontal rules.")
st.divider()  # Another horizontal rule






























