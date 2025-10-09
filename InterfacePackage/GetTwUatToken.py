import requests
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书安全警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_access_token():
  # 配置基础请求接口
  url = "https://openapi-idp-uat.auth.ap-northeast-1.amazoncognito.com/oauth2/token"
  # 配置基础入参
  payload = 'client_id=780j5q80h81v3d5humpjthejot&grant_type=client_credentials&scope=ecom%2Fapi.all&client_secret=1vries2lt5q10h9odfoq6rvdo0o9gl6ivireh43k08d01k5p2pep'
  # 配置请求头
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'XSRF-TOKEN=ab6edfc1-ab70-465f-9c28-3758bf5438fb'
  }

  # 发送请求获取token
  response = requests.post(url, headers=headers, data=payload, verify=False)
  # 提取access_token
  # 将响应内容解析为JSON字典
  token_data = response.json()
  # 获取【access_token】这个返参中的值
  return token_data["access_token"]

print(get_access_token())
