import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber在纽约市的搭车数据')


# 设置日期/时间列的名称
DATE_COLUMN = 'date/time'

@st.cache_data
def load_data(nrows):
    # 从指定URL下载数据，并将其加载到数据帧中
    data = pd.read_csv('./data/uber-raw-data-sep14.csv', nrows=nrows)

    # 将列名称转换为小写
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)

    # 将日期/时间列转换为日期时间类型
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    # 返回加载的数据帧
    return data


# 创建一个文本元素, 告诉读者数据正在加载中
data_load_state = st.text("正在加载数据...")

data = load_data(10000)

string = data.to_json()

data_load_state.text("Done! (using st.cache_data)")



if st.checkbox('显示原始数据'):
    # 添加子标题
    st.subheader('原始数据')
    # 打印原始数据
    st.write(data)


st.subheader('每小时乘车次数')

# 使用NumPy生成一个直方图，按小时统计乘车时间
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

# 通过Streamlit的st.bar_chart()方法绘制直方图
st.bar_chart(hist_values)



st.subheader('Map of all pickups')
st.map(data)

#hour_to_filter = 17
hour_to_filter = st.slider('选择小时', 0, 23, 17)  # min: 0h, max: 23h, 默认为 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'{hour_to_filter}:00时的所有乘车点地图')
st.map(filtered_data)

