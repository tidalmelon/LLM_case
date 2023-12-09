import streamlit as st
import pandas as pd



st.subheader('1.显示HTML的内容')
st.write("<h1 style='color: blue;'>这是HTML内容</h1>", unsafe_allow_html=True)


st.subheader('2.显示Markdown的内容')
st.write("这是一个列表：\n\n- 项目1\n- 项目2\n- 项目3")

st.subheader("3. 显示代码块")

code = '''
def hello_world():
    print("Hello, World!")

hello_world()
'''

st.code(code, language='python')



st.subheader("4. 显示DataFrame的交互式表格")


data = {'姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 28],
        '城市': ['北京', '上海', '广州']}

df = pd.DataFrame(data)

st.write(df)




st.subheader("5. 显示音频和视频")

audio_file = open('./data/Studio_Project_V1.mp3', 'rb')
st.write("这是一段音频：")
st.audio(audio_file, format='audio/mp3')

video_file = open('./data/shuitun.mp4', 'rb')
st.write("这是一段视频：")
st.video(video_file, format='video/mp4')

st.subheader("6. 显示图表")

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

st.write(fig)

st.subheader("7. 显示图表")

#from PIL import Image
#import streamlit as st
#
## 加载本地图片文件
#image = Image.open("image.jpg")
#
## 使用st.write()函数显示图片
#st.write("显示本地图片文件")
#st.write(image)
#
#
## 图片URL链接
#image_url = "https://example.com/image.jpg"
#
## 使用st.write()函数显示图片
#st.write("显示URL链接中的图片")
#st.write(f"![Image]({image_url})")



st.subheader("8. 显示地图")


# 获取地理位置的纬度和经度
latitude = 40.7128
longitude = -74.0060

# 使用 st.write() 函数显示地图
st.write(f"纬度：{latitude}, 经度：{longitude}, 没有谷歌地图的api_key")
#st.write(f"![Map](https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=13&size=300x300&markers=color:red%7Clabel:C%7C{latitude},{longitude}&key=YOUR_API_KEY)")




st.subheader("9. 显示PDF文件")

st.write("<h1 style='color: blue;'>需要处理较大的 PDF 文件或者需要更高级的 PDF 渲染和交互功能，建议使用专门的 PDF 处理库，如 PyMuPDF 或 pdf2image</h1>", unsafe_allow_html=True)


## 读取 PDF 文件的二进制数据
#with open("./data/part.pdf", "rb") as f:
#    pdf_bytes = f.read()
#
## 使用 st.write() 函数显示 PDF 文件
#st.write(pdf_bytes, format="pdf")





st.subheader("10. 显示文件下载链接")
st.write("<h1 style='color: blue;'>尽管使用 st.write() 函数创建下载链接是一种方法，但 Streamlit 也提供了 st.download_button() 和 st.file_downloader()</h1>", unsafe_allow_html=True)

file_url = "./data/shuitun.mp4"

# 在 st.write() 中添加文件下载链接
st.write(f"点击[此处]({file_url})下载文件, **本地相对地址没有效果**")







































