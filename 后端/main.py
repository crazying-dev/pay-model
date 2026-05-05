import socket
import atexit
import json
import time

IP = "0.0.0.0"
PORT = 1213
Time_over = 5
max_conn = 5

debug = True

shop_list = []

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

class web:
	def __init__(self):
		# 1.定义类型
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		log("定义TCP协议套接字")
		# 2.启动复用
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		log("启动端口复用")
		# 3.监听端口
		self.server_socket.bind((IP, PORT))
		log(f"监听地址:{IP}:{PORT}")
		# 4.设置超时
		self.server_socket.settimeout(Time_over)
		log(f"设置超时{Time_over}")
		# 5.设置最大连接数
		self.server_socket.listen(max_conn)
		log(f"设置最大连接数{max_conn}")
		
		# 6.注册自关闭
		atexit.register(self.server_socket.close)
		log("注册自关闭")
		
		# 7.启动主服务
		log("启动服务")
		self.main()

	def main(self):
		while True:
			try:
				conn, addr = self.server_socket.accept()
				data = json.loads(conn.recv(1024).decode("utf-8"))
				ID = data["ID"]
				log(f"收到用户订单信息,订单ID{ID},原始数据{data}")
				List = ""
				for i in data["items"]:
					shop = i["shop_id"]
					if shop not in shop_list:
						conn.send("0x000".encode("utf-8"))
					else:
						List += "{:<10} {:<15} {:<20}\n".format(shop,i["item_id"], i["other"])
				log(f"ID为{ID}的订单信息:{List}")
			except socket.timeout:
				continue
			except Exception as e:
				log(e)
				continue

if __name__ == '__main__':
	web = web()
