# python 3.6

import random
import time
import asyncio
import logging
# 配置日志
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'rasp-python-mqtt-streamlit'
client=None

deviceOnlineDic={
    "character/1":False,
    "character/2":False,
    "character/3":False,
    "pullVine/vine1":False,
    "pullVine/vine2":False,
    "mogu/servo":False,

}

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def messageCallback(client, userdata, msg):
    global correctAns,correctAns2,usrAns,deviceOnlineDic

    payload:str=msg.payload.decode()
    print(f"Received `{payload}` from `{msg.topic}` topic")


    if msg.topic=="report/all":
        if "live" in payload:
            deviceName=payload.split(":")
            deviceOnlineDic[deviceName[0]]=True
            print(deviceOnlineDic)

def init():
    """
    一开始调用一次
    """
    global client
    print("初始化MQTT")
    client = connect_mqtt()
    client.loop_start()
    client.subscribe("report/all")
    client.on_message=messageCallback

    asyncio.run(main())

async def periodic_checkAlive():
    """
    每隔30s检查所有设备是否在线
    """
    while True:
        # 在这里执行您想要定期执行的操作
        logging.info("检查所有设备是否在线")
        checkAllLive()

        # 暂停10秒
        await asyncio.sleep(30)


# 创建事件循环
async def main():
    # 启动协程
    task = asyncio.create_task(periodic_checkAlive())

    # 等待协程完成（这里可以添加其他操作）
    await task


def vinelightControl(isLight:bool,vineIndex:int):
    """
    控制藤蔓发不发光
    """
    global client
    
    assert client is not None

    thistopic=f"pullVine/vine{vineIndex}"

    msg=f"light{'up' if isLight else 'down'}"
    client.publish(thistopic,msg)

def dropPuzzleSlice():
    """
    控制舵机掉落碎片
    """
    global client
    assert client is not None

    
    thistopic="mogu/servo"
    client.publish(thistopic,"drop")

def checkAllLive():
    """
    检查是否所有设备都在线
    """
    global client
    assert client is not None
    
    topicList=[
        "character/all",
        "mogu/servo",
    ]
    for name in topicList:
        client.publish(name,"ISONLINE")





    

if __name__ == '__main__':
    init()