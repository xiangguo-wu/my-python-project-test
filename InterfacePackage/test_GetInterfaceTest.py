import pytest#导入pytest框架
import requests#导入https接口请求模块
import json#入参和返参使用json格式，需要用到这个模块
import GetTwUatToken#导入自动生成token模块
import urllib3#导入禁用SSL告警模块
from urllib3.util.retry import Retry#导入重置机制模块
import socket#导入设定超时等待时间模块
from requests.adapters import HTTPAdapter#导入requests模块中的https请求适配型的方法


# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#增加超时时间
#设置30秒超时，给服务器更多响应时间
#避免因网络延迟导致请求过早失败
socket.setdefaulttimeout(30)

# 创建并配置Session对象（统一放在前面）
session = requests.Session()#使用requests模块中的Session方法，也就是通过Session方法来处理http请求
session.verify = False  # 禁用SSL验证，统一设置verify=False确保所有请求都跳过SSL验证

# 配置重试机制（统一放在前面）
# 添加重试机制，这是最关键的一步！自动重试机制解决了网络波动问题
# 当遇到429（太多请求）或5xx服务器错误时自动重试
# 重试3次，每次间隔时间递增（backoff_factor=1）
retry_strategy = Retry(
    total=3,  # 最大重试次数
    backoff_factor=1,  # 重试间隔因子
    status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的状态码
)

adapter = HTTPAdapter(max_retries=retry_strategy) # 使用requests.adapters的HTTPAdapter方式
session.mount("https://", adapter)  # 使用session库的mount方法，为HTTPS请求添加适配器

# 基础配置请求地址
base_url = "https://tw-openapi-uat.intranet.local"
endpoint = "/uat/user-center-lifecycle/userInfo/v1/queryMemberInfo"
get_url = base_url + endpoint#请求接口信息放在一个变量中，方便后续测试用例统一调用

# 创建请求头，请求头放在一个变量中，方便后续测试用例统一调用
# 因为token每1h会过期，所以取另外一个模块的获取token结果作为Authorization（也就是token）
qingqiutou = {
    'x-apigw-api-id': 'trql10f0a1',
    'x-api-key': 'A7K7PMSAR237STANCBK8',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {GetTwUatToken.get_access_token()}',
    'Host': 'tw-openapi-uat.intranet.local'
}

# 测试用例1：查询有效case，例如ada传"9922705"
def test_TestCase1_youxiaoyonghu():
    print("\n执行测试用例1：查询有效用户")

    # 准备请求数据（测试步骤的数据）
    rucan = json.dumps({
        "searchKeys": [{"type": "aboNumber", "value": "9922705"}],
        "scope": ["basic", "applicant", "extend", "phone", "email"],
        "regionCode": "130",
        "channel": "INT",
        "bizCode": "INT",
        "language": "zh-CN"
    })

    # 发送请求
    # 使用预先配置好的session发送请求
    # 因为我们这里使用了session，加强了连接的会话稳定性；如果不使用的话，就正常使用requests.get或者requests.post
    # get请求和post请求都有对应的参数标准
    response = session.post(get_url, headers=qingqiutou, data=rucan, timeout=30)

    # 请求结果以json的形式返回，赋值到变量response_json中
    response_json = response.json()

    # 预期检查点1：验证HTTP状态码，这是https请求中返回的，和业务返参无关，算是一条通用case，相当于是验证接口是否可以调通的判断
    assert response.status_code == 200, f"HTTP状态码错误: {response.status_code}"
    print("HTTP状态码验证通过 (200)")

    # 预期检查点2：验证业务状态码
    assert response_json["code"] == "0", f"业务状态码错误: {response_json['code']}"
    print("业务状态码验证通过 (0)")

    # 预期检查点3：验证message字段
    assert response_json["message"] == "success", "message"
    print("message字段验证通过 (success)")


# 测试用例1：查询无效case，例如ada传"aaa"
def test_TestCase2_wuxiaoyonghu():
    print("\n执行测试用例2：查询无效用户")

    # 准备请求数据（测试步骤的数据）
    rucan = json.dumps({
        "searchKeys": [{"type": "aboNumber", "value": "aaa"}],
        "scope": ["basic", "applicant", "extend", "phone", "email"],
        "regionCode": "130",
        "channel": "INT",
        "bizCode": "INT",
        "language": "zh-CN"
    })

    # 发送请求
    # 使用预先配置好的session发送请求
    # 因为我们这里使用了session，加强了连接的会话稳定性；如果不使用的话，就正常使用requests.get或者requests.post
    # get请求和post请求都有对应的参数标准
    response = session.post(get_url, headers=qingqiutou, data=rucan, timeout=30)

    # 请求结果以json的形式返回，赋值到变量response_json中
    response_json = response.json()

    # 预期检查点1：验证HTTP状态码，这是https请求中返回的，和业务返参无关，算是一条通用case，相当于是验证接口是否可以调通的判断
    assert response.status_code == 200, f"HTTP状态码错误: {response.status_code}"
    print("HTTP状态码验证通过 (200)")

    # 预期检查点2：验证业务状态码
    assert response_json["code"] == "UC.P.ABO_NUMBER_FORMAT_ERROR.01", f"业务状态码错误: {response_json['code']}"
    print("业务状态码验证通过 (UC.P.ABO_NUMBER_FORMAT_ERROR.01)")

    # 预期检查点3：验证message字段
    assert response_json["message"] is None, "message字段应为null"
    print("message字段验证通过 (null)")