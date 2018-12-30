# easyHTTP
easy use tornado client and server

# 安装

python3.6

tornado5.0.4

下载
```shell
python setup.py install
```

# 使用
## client
### Client

```python
"""获取baidu.com 页面内容"""
from easyHTTP.client import Client,ContentType

class ExampleClient(Client):
    METHOD = "GET"
    CONTENT_TYPE = ContentType.JSON
    RESPONSE_CONTENT_TYPE = None
    TIMEOUT = 0
    FOLLOW_REDIRECTS = True

    def transform(self, resp_data):
        return resp_data

# 异步调用
await ExampleClient().call('https://baidu.com/')
# 同步调用
ExampleClient().
('https://baidu.com/')
```
> 类变量

`METHOD` method方法  
`CONTENT_TYPE` 指定http的请求content_type  
`RESPONSE_CONTENT_TYPE`: 指定http返回的数据解析格式，默认会通过response的content_type自动识别  
`TIMEOUT`: 超时时间  
`FOLLOW_REDIRECTS`: 302返回时是否自动再次请求redirect_url,默认是  

> 函数

**transform(self, resp_data)**  
`resp_data` 解析出来的返回结果  
需要使用方自定义，默认返回response的body  

**async def call(self, url=None, data=None, headers=None)**  
异步调用client获取详情  
`url` 请求url  
`data` dict http的body  
`headers` dict http的头  

返回是`transform` 定义的返回内容

**call_sync** . 
`call`的同步版

### RedirectClient
继承`Client`, 获取302跳转url，使用Header中的`Location`

### API
`Client`基本已经够用 . 
`API` 继承 `Client`，可以更好自定义url的内容

增加类变量 . 
`HOST` server的地址，如 "https://api.github.com/"  
`PATH` 路径，支持format  

**async def call(self, path_args=None, params=None, data=None,headers=None)**  
`path_args` 传递`PATH`中指定的变量  
`params` query 参数  
`data`,`headers` 同`Client`  

### FileClient
下载文件  
调用`call`返回dict
```
{
"filename": "文件名",
"content": "文件内容",
"size": 0# 文件大小
}
```

### Session
管理Client的cookie


```python
from easyHTTP.client import API,Session

cookies = {"CK1": "VALUE"}
se = Session(cookies)  

se.call(Client,"http://baidu.com/")
se.call(Client,"http://baidu.com/other_page") # 参数和

```

`cookie` 成员变量，获取当前cookie数据

**async def call(self, client, *args, \*\*kwargs)**  
`client` 如 `Client`,`API`,`FileClient`  
其他参数和client一致  

## server
