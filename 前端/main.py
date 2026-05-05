import socket
import json
from typing import Union
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1213

a = {"time": time.time(),"ID": Union[str,int],"items": [{"shop_id": Union[str,int],"item_id" :Union[str,int],"other": str}]}

def send_order():
    try:
        # 创建TCP客户端
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))

        # 字典 → JSON字符串 → 二进制
        send_data = json.dumps(a).encode("utf-8")
        client.send(send_data)

        # 接收服务器返回结果
        res = client.recv(1024).decode("utf-8")

        client.close()

    except Exception as e:
        print(e)

if __name__ == '__main__':
    send_order()