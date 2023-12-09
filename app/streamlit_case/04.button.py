import streamlit as st
import pandas as pd
import time


markdown = """
### 适合将if st.button()嵌套在里面的场景包括：
* 瞬时消失的消息：一旦按钮被点击，显示消息但立即消失。
* 每次点击后执行的过程：将数据保存到会话状态、文件或数据库

### 而不适合将if st.button()嵌套在里面的场景包括：
* 需要在用户继续操作时保留的显示项。
* 引起脚本重新运行的其他小部件使用。
* 既不修改会话状态也不写入文件/数据库的过程*。（*当需要一次性结果时，这种情况也可以接受。例如，如果你有一个“验证”按钮，可以将它作为直接依赖于按钮的流程，用于创建一个弹出消息，告诉用户’有效’或’无效’，而不需要保留这些信息。）
"""

st.markdown(markdown)



st.subheader('1. 通过按钮显示临时消息的常用逻辑')

animal_shelter = ['cat', 'dog', 'rabbit', 'bird']

animal = st.text_input('输入一个动物')

if st.button('检查可用性'):
    have_it = animal.lower() in animal_shelter
    '我们有这个动物！' if have_it else '我们没有这个动物。'



st.subheader('2. 状态保留按钮')

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('点击我', on_click=click_button, key="1")

if st.session_state.clicked:
    # 消息和嵌套小部件将保留在页面上
    st.write('按钮已点击！')
    st.slider('选择一个值')


st.subheader('3. 切换按钮')

if 'button' not in st.session_state:
    st.session_state.button = False

# 取反
def click_button_not():
    st.session_state.button = not st.session_state.button


# 注意哦 如果不分配 key 会报: DuplicateWidgetID: There are multiple identical st.button widgets with the same generated key.
st.button('点击我', on_click=click_button_not, key="2")

if st.session_state.button:
    # 消息和嵌套小部件将保留在页面上
    st.write('按钮已打开！')
    st.slider('选择一个值')
else:
    st.write('按钮已关闭！')


st.subheader("4. 控制流程的按钮-回调函数传参数")

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:
    st.button('开始', on_click=set_state, args=[1], key='3')

if st.session_state.stage >= 1:
    name = st.text_input('姓名', on_change=set_state, args=[2])

if st.session_state.stage >= 2:
    st.write(f'你好，{name}！')
    color = st.selectbox(
        '选择一种颜色',
        [None, '红色', '橙色', '绿色', '蓝色', '紫色'],
        on_change=set_state, args=[3]
    )
    if color is None:
        set_state(2)

if st.session_state.stage >= 3:
    st.write(f'😊谢谢你，{color}！')
    st.button('重新开始', on_click=set_state, args=[0], key='4')


st.subheader("5. 动态添加小部件的按钮")


def display_input_row(index):
    left, middle, right = st.columns(3)
    left.text_input('First', key=f'first_{index}')
    middle.text_input('Middle', key=f'middle_{index}')
    right.text_input('Last', key=f'last_{index}')

if 'rows' not in st.session_state:
    st.session_state['rows'] = 0

def increase_rows():
    st.session_state['rows'] += 1

st.button('Add person', on_click=increase_rows, key='5')

for i in range(st.session_state['rows']):
    display_input_row(i)

st.subheader('People list')
for i in range(st.session_state['rows']):
    st.write(
        f'Person {i+1}:',
        st.session_state[f'first_{i}'],
        st.session_state[f'middle_{i}'],
        st.session_state[f'last_{i}']
    )




st.subheader("6. 使用按钮处理耗时或写入文件的过程")
st.write("st.session_state中的结果仅对当前用户的当前会话可见。如果使用st.cache_data代替，结果将对所有用户和所有会话可见。")

def expensive_process(option, add):
    with st.spinner('Processing...'):
        time.sleep(5)
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C':[7, 8, 9]}) + add
    return (df, add)


cols = st.columns(2)
option = cols[0].selectbox('Select a number', options=['1', '2', '3'])
add = cols[1].number_input('Add a number', min_value=0, max_value=10)

if 'processed' not in st.session_state:
    st.session_state.processed = {}

if st.button('Process', key='6'):
    result = expensive_process(option, add)
    st.session_state.processed[option] = result

if option in st.session_state.processed:
    st.write(f'Option {option} processed with add {add}')
    st.write(st.session_state.processed[option][0])


st.subheader("7. [常见的错误做法，需要格外注意](https://blog.csdn.net/weixin_46043195/article/details/132115271)")

















