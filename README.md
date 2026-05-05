# 订单交易模块

前端: ./前端/main.py
后端: ./后端/main.py

> 端口号 ：1213  
> IP ： 未知 （暂定回环地址127.0.0.1）
> 
> 协议 ： TCP

错误编码

| 编码    | 含义    |
|-------|-------|
| 0x000 | 店名不正确 |


商品信息数据传输格式
```python
from typing import Union
import time

a = {
    "time": time.time(),
    "ID": Union[str,int],
    "items": [
	    {
            "shop_id": Union[str,int],
            "item_id" :Union[str,int],
            "other": str
        }
    ]
}
```

