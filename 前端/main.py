import socket
import json
import uuid
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1213

debug = True


class Tool:
	def __init__(self):
		self.log("日志初始化成功")
		self.log("服务准备启动")
	
	def log(self, message):
		if debug:
			Now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			print(f"[{Now}] {message}")


tool = Tool()
log = tool.log

# 全局订单数据
a = {"time": time.time(), "items": []}

def main(shops_id: list, item_ids: list, others: list):
	global a
	if len(item_ids) == len(shops_id) == len(others):
		a["ID"] = str(uuid.uuid4())
		a["items"] = []  # 清空避免重复
		for n in range(len(shops_id)):
			shop_id = shops_id[n]
			item_id = item_ids[n]
			other = others[n]
			a["items"].append({
				"shop_id": shop_id,
				"item_id": item_id,
				"other": other
			})

def send():
	try:
		# 创建TCP客户端
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((SERVER_IP, SERVER_PORT))
		log(f"连接服务端成功")

		total = len(a["items"])
		# 1. 先发送首包（必须发！）
		first_packet = {
			"ID": a["ID"],
			"time": time.time(),
			"all": total
		}
		send_data = json.dumps(first_packet)[::-1].encode("utf-8")
		client.send(send_data)
		time.sleep(0.1)

		# 2. 循环发送所有商品包（索引从0开始）
		for i in range(total):
			item_packet = {
				"ID": a["ID"],
				"time": time.time(),
				"item": a["items"][i],
				"all": total,
				"now": i + 1  # 第1、2、3...包
			}
			send_data = json.dumps(item_packet)[::-1].encode("utf-8")
			client.send(send_data)
			time.sleep(0.1)

		# 3. 接收服务端返回结果
		res = client.recv(1024)[::-1].decode("utf-8")
		print(f"服务端返回：{res}")

		client.close()

	except Exception as e:
		print(f"客户端异常：{e}")

if __name__ == '__main__':
	# 传入3个订单
	main([0000, 0000], [ 10200, 200810], [ 111, "www"])
	send()