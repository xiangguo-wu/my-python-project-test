
import requests
import json
import urllib3
import socket

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)###很重要，很多时候访问公司内网，经常会因为SSL导致无法访问

# 设置更长的超时时间
socket.setdefaulttimeout(30)

url = "https://tw-openapi-uat.intranet.local/uat/user-center-lifecycle/userInfo/v1/queryMemberInfo"

payload = json.dumps({
    "searchKeys": [
        {
            "type": "aboNumber",
            "value": "9922705"
        }
    ],
    "scope": [
        "basic",
        "applicant",
        "extend",
        "phone",
        "email"
    ],
    "regionCode": "130",
    "channel": "INT",
    "bizCode": "INT",
    "language": "zh-CN"
})

headers = {
    'x-apigw-api-id': 'trql10f0a1',
    'x-api-key': 'A7K7PMSAR237STANCBK8',
    'Content-Type': 'application/json',
    'Authorization': 'eyJraWQiOiIyM0g3QXNEeEQya1Rya2RIa2hWUFhBY2toOHoxQ3Vhdjg3TWVSNlpiZFBjPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3ODBqNXE4MGg4MXYzZDVodW1wanRoZWpvdCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiZWNvbVwvYXBpLmFsbCIsImF1dGhfdGltZSI6MTc1ODgwOTQ0MiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLW5vcnRoZWFzdC0xX3BIN002Rm9FNyIsImV4cCI6MTc1ODg1MjY0MiwiaWF0IjoxNzU4ODA5NDQyLCJ2ZXJzaW9uIjoyLCJqdGkiOiJkZTAxM2YxNS1iMzE3LTQ1NTQtYTlhNS1kZmZkYTBhNWQzNjEiLCJjbGllbnRfaWQiOiI3ODBqNXE4MGg4MXYzZDVodW1wanRoZWpvdCJ9.SLDiD2d-JB2b1ZE6mgGPmTxeTveIACy1AJtwoXfuzaQFOnUqQLWpgVX2DzUiXae85J1GEK--K_621HrI89ERtDFM4cmxUopvzhHYC7zL1lshMuIBkl35I_Z3DYXSPC4XrGobJFdb80PLR-jGWogBefSM7w9wPHrL3YiPoYvbo7gSNQ-oQJX86yB5-4Ece4QEO_yzz2tz_9NLDp4ts9LGAPnRB5KHg23IGElMfIyl3_0RK_UfCfwDpszl-KMmrI5EsJWQ590syijrGTaPSNm-CyHbQc5DFCUnlcJQhgtMvFXR9BO6rCachjEe49RhAvJUfGYmTEpS9Q5UZ8sSU3QPZQ',
    'Host': 'tw-openapi-uat.intranet.local'  # 添加Host头，明确指定Host头，帮助API网关正确路由请求，特别是当使用IP地址时，这个头非常重要
}

try:
    # 使用session并配置不验证SSL
    session = requests.Session()
    session.verify = False###统一设置verify=False确保所有请求都跳过SSL验证

    # 添加重试机制，这是最关键的一步！自动重试机制解决了网络波动问题
    # 当遇到429（太多请求）或5xx服务器错误时自动重试
    # 重试3次，每次间隔时间递增（backoff_factor=1）
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    #增加超时时间
    #设置30秒超时，给服务器更多响应时间
    #避免因网络延迟导致请求过早失败
    response = session.post(url, headers=headers, data=payload, timeout=30)

    if response.status_code == 200:
        print("请求成功！")
        print("返回结果:", response.json())
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)

except Exception as e:
    print(f"发生异常: {str(e)}")
    print("建议检查:")
    print("1. 确保VPN连接稳定")
    print("2. 尝试使用IP地址代替域名")
    print("3. 联系网络管理员确认内部域名解析")
