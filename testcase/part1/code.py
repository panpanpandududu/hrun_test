import base64
import uuid
import json
from PIL import Image
import base64
import requests

# 下载图片到本地
uid = uuid.uuid4()
url = 'https://XXX/auth/login/verifycode/image?mobile=e579ad6d-9453-4dc6-80b3-597bd063d442'
headers = {
    'X-Ca-Nonce': str(uid),
    'Authorization': 'APPCODE XXX'
}
ret = requests.get(url, headers=headers, verify=False)
print(json.loads(ret.text)['data'])
# 通过接口获取base64加密的图片
data = json.loads(ret.text)['data']
image_data = base64.b64decode(data)
# 将图片写入到本地
with open('1.png', 'wb') as f:
    f.write(image_data)
#


def binarizing(img, threshold):
    img = img.convert("L")  # 转灰度
    pixdata = img.load()
    w, h = img.size
    # 遍历所有像素，大于阈值的为黑色
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


def depoint(img):
    # 传入二值化后的图片进行降噪
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:  # 上
                count = count + 1
            if pixdata[x, y + 1] > 245:  # 下
                count = count + 1
            if pixdata[x - 1, y] > 245:  # 左
                count = count + 1
            if pixdata[x + 1, y] > 245:  # 右
                count = count + 1
            if pixdata[x - 1, y - 1] > 245:  # 左上
                count = count + 1
            if pixdata[x - 1, y + 1] > 245:  # 左下
                count = count + 1
            if pixdata[x + 1, y - 1] > 245:  # 右上
                count = count + 1
            if pixdata[x + 1, y + 1] > 245:  # 右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img


# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=XXX&client_secret=GiPHDG20zdp5aIhwH4CGZsWmaNdqptNQ'
response = requests.get(host, verify=False)
print(response.text)
access_token = json.loads(response.text)['access_token']

# 首先对图片进行降噪处理
p1 = Image.open('1.png')
p1 = binarizing(p1, 170)
p1 = depoint(p1)
p1.show()
p1.save('1.png')

# 二进制方式打开图片文件
f = open('1.png', 'rb')
img = base64.b64encode(f.read())

# 图像识别,使用百度的精准识别
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
params = {"image": img}
access_token = json.loads(response.text)['access_token']
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params,
                         headers=headers, verify=False)
if response:
    vefiry_code = []
    # 去除两边空格
    code = (response.json()['words_result'][0]['words']).strip()
    #  识别图片中可能存在空格，去空格
    for i in code:
        if i != ' ':
            vefiry_code.append(i)
    code = ''.join(vefiry_code)
    print(code)
