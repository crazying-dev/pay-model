import socket
import json
import uuid
from typing import Union
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1213


a = {"time": time.time(),"items": []}

def main(shops_id:list, item_ids:list, others:list):
	global a
	if len(item_ids) == len(shops_id) == len(others):
		a["ID"] = str(uuid.uuid4())
		n = 0
		for item_id in item_ids:
			shop_id = shops_id[n]
			other = others[n]
			a["items"].append({"shop_id": shop_id,"item_id" :item_id,"other": other})
	

def send():
	try:
		# 创建TCP客户端
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((SERVER_IP, SERVER_PORT))

		# 字典 → JSON字符串 → 二进制
		send_data = json.dumps(a)[::-1].encode("utf-8")
		client.send(send_data)

		# 接收服务器返回结果
		# res = client.recv(1024)[::-1].decode("utf-8")

		client.close()

	except Exception as e:
		print(e)

if __name__ == '__main__':
	main([0000], [1000], [None])
	send()
	