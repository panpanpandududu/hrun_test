import hashlib
import time
from utils.connect_mysql import DbConnect, dbinfo


# debugtalk 传参，生成测试数据
def get_user():
    return [
        {"user": "test1"},
        {"user": "test2"},
        {"user": "test3"}
    ]


def get_psw():
    return [
        {"psw": "123456"}
    ]


def get_user_psw(num):
    accounts = []
    for i in range(1, num + 1):   #range(start,stop)  #不包括stop
        accounts.append(
            {'user': "test%s" % i,
             'psw': "123456"}
        )
    return accounts


# 生成带时间戳的注册账号
def register_user():
    ''' 生成带时间戳的注册账号'''
    user = "test"+str(int(time.time()))
    time.sleep(1)
    return user

#随机生成商品编号
def goods_code():
    time.sleep(1)
    goodscode = "sp_" + str(int(time.time()*100))
    return goodscode

# hook机制
def setup_hook():
    print("----请求预处理----")  # 比如加密


def teardown_hook():
    print("----返回预处理----")  # 比如解密
    # 接口返回后对接口返回数据进行处理，比如把状态码200改成203


# 接口请求预处理
def request_sign(dicts):
    body = dicts.get("req_json")  # get() 方法返回具有指定键的项目值

    """
    request内容
    {
    'method': 'POST',
    'url': '/api/v1/login',
    'params': {},
    'headers': {'HRUN-Request-ID': 'HRUN-66b36821-e868-44dc-b3b9-1d29b6abca62-517959'},
    'req_json': {'username': 'test1', 'password': '123456'},
    'data': None,
    'cookies': {},
    'timeout': 120,
     'allow_redirects': True,
      'verify': False
      }
    """
    print("body内容", body)
# body内容 {'username': 'test1', 'password': '123456'}

    # 添加签名
    sign = "1234xxxxx"
    body['sign'] = sign
    dicts["req_json"] = body
    print("request内容", dicts)


# 接口响应预处理
def response_status(response):
    '''修改返回状态码'''
    print("返回response status_code", response.status_code)
    response.status_code = 203
    print("返回修改后的response status_code", response.status_code)


# 签名安全验证
def sign_body(body, apikey="12345678"):  # 先拼接字符串，再加密
    '''请求body sign签名'''
    # 列表生成式，生成key=value格式
    a = ["".join(i) for i in body.items() if i[1] and i[0] != "sign"]
    # print(a)
    # 参数名ASCII码从小到大排序
    strA = "".join(sorted(a))
    # print(strA)

    # 在strA后面拼接上apiKey得到striSignTemp字符串
    striSignTemp = strA+apikey

    # MD5加密 封装方法加密

    def jiamimd5(src):
        m = hashlib.md5()  # 获取一个md5加密算法对象
     # 制定需要加密的字符串  hashlib是对二进制进行加密的，如果直接对字符串加密的话， 会报错的。因此需要通过encode将字符串转码成二进制格式
        m.update(src.encode('UTF-8'))  # 加密
        return m.hexdigest()  # 获取加密后的16进制字符串

    sign = jiamimd5(striSignTemp.lower())  # 将strSignTemp字符串转换为小写字符串后进行MD5运算
    # print(sign)
    return sign


# 封装接口传参加密
def get_sign(request):
    body = request.get("req_json")
    sign = sign_body(body)
    request["req_json"]["sign"] = sign


# 连接数据库，进行数据库的增删改查

def get_db_goods(id, key="goodsstatus"):
    db = DbConnect(dbinfo, database="apps")  # 实例化对象
    sql1 = "SELECT * FROM apiapp_goods WHERE id =%s" % id
    res1 = db.select(sql1)
    print(res1)
    if len(res1) == 0:
        result = ''
    else:
        result = res1[0][key]
    return result


if __name__ == '__main__':
    body = {
        "username": "test",
        "password": "123456"
    }
    # print(get_db_info(1))
    str = "*****this is **string** example....wow!!!*****"
    s = str.strip('"')
    print(type(s))

# print(sign_body(body))
# print(register_user())
