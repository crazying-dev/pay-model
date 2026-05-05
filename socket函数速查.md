# socket函数速查

| 函数	                           | 作用         |
|-------------------------------|------------|
| socket(AF_INET, SOCK_STREAM)	 | 创建 TCP 套接字 |
| socket(AF_INET, SOCK_DGRAM)	  | 创建 UDP 套接字 |
| bind((ip, port))	             | 绑定地址（服务端用） |
| listen(n)	                    | 开始监听       |
| accept()	                     | 等待客户端连接    |
| connect((ip, port))	          | 客户端连接服务端   |
| send(data)	                   | TCP 发送数据   |
| recv(size)	                   | TCP 接收数据   |
| sendto(data, addr)	           | UDP 发送数据   |
| recvfrom(size)	               | UDP 接收数据   |
| close()                       | 	关闭连接      |

# 字符串
| 功能        | 内容              |
|-----------|-----------------|
| 字符串 → 二进制 | encode("utf-8") |
| 二进制 → 字符串 | decode("utf-8") |