from paho.mqtt import client as mqtt_client
import time

broker = 'localhost'
port = 1883

client_id = f'rasp-python-autoRobot'
client=None

correctAns=set([6,4,1])
correctAns2=set([3,5,1])
usrAns=set([])

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

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        # msg = f"messages: {msg_count}"
        # result = client.publish(topic, msg)
        # # result: [0, 1]
        # status = result[0]
        # if status == 0:
        #     print(f"Send `{msg}` to topic `{topic}`")
        # else:
        #     print(f"Failed to send message to topic {topic}")
        # msg_count += 1

def subscribe(client: mqtt_client,topic):
    def on_message(client, userdata, msg):
        global correctAns,correctAns2,usrAns

        payload=msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")

# region 文字解密
        isCharacterSw=False
        if msg.topic=="report/character3":
            isCharacterSw=True
            if payload=="sw1":
                usrAns.add(6)
            if payload=="sw2":
                usrAns.add(7)
            if payload=="sw3":
                usrAns.add(8)
            
        if msg.topic=="report/character2":
            isCharacterSw=True
            if payload=="sw1":
                usrAns.add(4)
            if payload=="sw2":
                usrAns.add(5)

        if msg.topic=="report/character1":
            isCharacterSw=True
            
            if payload=="sw1":
                usrAns.add(1)
            if payload=="sw2":
                usrAns.add(2)
            if payload=="sw3":
                usrAns.add(3)
        if isCharacterSw:

            if usrAns==correctAns or usrAns==correctAns2:
                print("文字解密正确！点亮所有的灯")
                client.publish("character/all","correct")
                usrAns.clear()

            elif len(usrAns)>=3:
                print("文字解密答案不对，闪烁！")
                client.publish("character/all","wrong")
                usrAns.clear()

 #endregion       

    client.subscribe(topic)
    client.on_message = on_message


def run():
    init()
    subscribe(client,"report/character3")
    subscribe(client,"report/character2")
    subscribe(client,"report/character1")
    publish(client)

def init():
    """
    一开始调用一次
    """
    global client
    client = connect_mqtt()
    client.loop_start()

if __name__ == '__main__':
    run()