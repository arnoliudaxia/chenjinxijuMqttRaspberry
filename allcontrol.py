import streamlit as st
from mqttHelper import init,vinelightControl,checkAllLive,dropPuzzleSlice,deviceOnlineDic
import time

# if "isInitMqtt" not in st.session_state:
#     st.session_state["isInitMqtt"]=True
#     init()

if st.button("检查所有设备连接情况"):
    checkAllLive()
    # time.sleep(0.5)

st.success('藤蔓控制')
# if not deviceOnlineDic["pullVine/vine1"]:
#     st.error("藤蔓1离线！")
vineCols= st.columns(2)

with vineCols[0]:
    "参数表"
    "pullVine/vine1"
    """
    - lightup
    - lightdown
    """
with vineCols[1]:
    if st.button("打开灯光"):
        vinelightControl(True,1)
    if st.button("关闭灯光"):
        vinelightControl(False,1)

st.success('敲蘑菇装置')
moguCols= st.columns(2)

with moguCols[0]:
    # 显示装置离线和在线情况
    if deviceOnlineDic["mogu/servo"]:
        st.success("舵机在线")
        if st.button("掉落碎片"):
            dropPuzzleSlice()
    else:
        st.error("舵机离线")

