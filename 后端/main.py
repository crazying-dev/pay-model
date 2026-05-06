import socket
import atexit
import json
import time

IP = "0.0.0.0"
PORT = 1213
Time_over = 5
max_conn = 5

debug = True

# 合法商店ID列表
shop_list = [0000]


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
				log(f"客户端已连接：{addr}")
				
				# 接收首包（必须先收首包）
				first_data = conn.recv(1024).decode("utf-8")[::-1]
				data = json.loads(first_data)
				ID = data["ID"]
				all_count = data["all"]
				log(f"收到订单首包 ID:{ID}, 总包数:{all_count}")
				
				ALL = {"ID": ID, "items": []}
				last = 0  # 从0开始计数
				
				# 循环接收所有分包
				for itemcount in range(all_count):
					packet_data = conn.recv(1024).decode("utf-8")[::-1]
					data = json.loads(packet_data)
					
					# 校验包合法性
					if (data["ID"] == ID
							and data["all"] == all_count
							and data["now"] == last + 1):
						dataitem = data["item"]
						ALL["items"].append(dataitem)
						log(f"收到第{last + 1}份数据: {data}")
						last += 1
				
				# 校验所有商品ID是否合法
				List = ""
				valid = True
				for i in ALL["items"]:
					shop = i["shop_id"]
					if shop not in shop_list:
						valid = False
						break
					List += "{:<10} {:<15} {:<20}\n".format(
						shop,
						i["item_id"],
						i["other"] if i["other"] is not None else ""
					)
				
				# 给客户端回复结果
				if valid:
					log(f"订单 {ID} 校验通过\n{List}")
					conn.send("0y000".encode("utf-8")[::-1])  # 成功
				else:
					log(f"订单 {ID} 存在非法商店ID")
					conn.send("0x000".encode("utf-8")[::-1])  # 失败
				
				conn.close()
			
			except socket.timeout:
				continue
			except KeyboardInterrupt:
				log("服务手动关闭")
				self.server_socket.close()
				exit(0)
			except Exception as e:
				log(f"异常：{e}")
				continue


if __name__ == '__main__':
	web = web()