import pytest
import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def test_query_member_info():
    """测试用户信息查询接口返回数据"""
    # 1. 准备测试数据
    url = "https://tw-openapi-uat.intranet.local/uat/user-center-lifecycle/userInfo/v1/queryMemberInfo"
    payload = json.dumps({
        "searchKeys": [{"type": "aboNumber", "value": "9922705"}],
        "scope": ["basic", "applicant", "extend", "phone", "email"],
        "regionCode": "130",
        "channel": "INT",
        "bizCode": "INT",
        "language": "zh-CN"
    })

    # 使用当前时间戳标记测试
    test_start = time.strftime("%Y-%m-%d %H:%M:%S")

    headers = {
        'x-apigw-api-id': 'trql10f0a1',
        'x-api-key': 'A7K7PMSAR237STANCBK8',
        'Content-Type': 'application/json',
        'Authorization': 'eyJraWQiOiIyM0g3QXNEeEQya1Rya2RIa2hWUFhBY2toOHoxQ3Vhdjg3TWVSNlpiZFBjPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3ODBqNXE4MGg4MXYzZDVodW1wanRoZWpvdCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiZWNvbVwvYXBpLmFsbCIsImF1dGhfdGltZSI6MTc1ODgwOTQ0MiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLW5vcnRoZWFzdC0xX3BIN002Rm9FNyIsImV4cCI6MTc1ODg1MjY0MiwiaWF0IjoxNzU4ODA5NDQyLCJ2ZXJzaW9uIjoyLCJqdGkiOiJkZTAxM2YxNS1iMzE3LTQ1NTQtYTlhNS1kZmZkYTBhNWQzNjEiLCJjbGllbnRfaWQiOiI3ODBqNXE4MGg4MXYzZDVodW1wanRoZWpvdCJ9.SLDiD2d-JB2b1ZE6mgGPmTxeTveIACy1AJtwoXfuzaQFOnUqQLWpgVX2DzUiXae85J1GEK--K_621HrI89ERtDFM4cmxUopvzhHYC7zL1lshMuIBkl35I_Z3DYXSPC4XrGobJFdb80PLR-jGWogBefSM7w9wPHrL3YiPoYvbo7gSNQ-oQJX86yB5-4Ece4QEO_yzz2tz_9NLDp4ts9LGAPnRB5KHg23IGElMfIyl3_0RK_UfCfwDpszl-KMmrI5EsJWQ590syijrGTaPSNm-CyHbQc5DFCUnlcJQhgtMvFXR9BO6rCachjEe49RhAvJUfGYmTEpS9Q5UZ8sSU3QPZQ',
        'Host': 'tw-openapi-uat.intranet.local',
        'X-Test-Start-Time': test_start
    }

    try:
        # 2. 发送请求（带重试机制）
        session = requests.Session()
        session.verify = False  # 跳过SSL验证

        # 配置自动重试
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        print(f"测试开始时间: {test_start}")
        print("正在发送请求...")
        response = session.post(url, headers=headers, data=payload, timeout=30)
        print(f"请求完成，状态码: {response.status_code}")

        # 3. 验证响应状态码
        assert response.status_code == 200, (
            f"请求失败，状态码: {response.status_code}\n"
            f"响应内容: {response.text[:500]}"
        )

        # 4. 解析响应数据
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            pytest.fail("响应不是有效的JSON格式")

        print("接口返回数据:", json.dumps(response_data, indent=2, ensure_ascii=False))

        # 5. 验证关键业务字段（根据实际返回结构调整）
        # 确保响应有data字段且是列表
        assert 'data' in response_data, "响应缺少data字段"
        assert isinstance(response_data['data'], list), "data字段不是列表类型"
        assert len(response_data['data']) > 0, "data列表为空"

        # 获取第一个结果
        first_result = response_data['data'][0]

        # 确保有details字段且是列表
        assert 'details' in first_result, "响应缺少details字段"
        assert isinstance(first_result['details'], list), "details字段不是列表类型"
        assert len(first_result['details']) > 0, "details列表为空"

        # 获取第一个detail
        first_detail = first_result['details'][0]

        # 确保返回的用户ID匹配
        assert 'basic' in first_detail, "响应缺少basic字段"
        assert 'aboNumber' in first_detail['basic'], "响应缺少aboNumber字段"
        assert first_detail['basic']['aboNumber'] == "9922705", (
            f"用户ID不匹配，预期: 9922705, 实际: {first_detail['basic'].get('aboNumber')}"
        )

        # 确保基础信息存在（basic字段已在上面验证）

        # 确保返回的scope包含请求的字段
        requested_scopes = ["basic", "applicant", "extend", "phone", "email"]
        missing_scopes = [scope for scope in requested_scopes if scope not in first_detail]

        # 注意：实际返回中电话字段是"bindPhones"而不是"phone"
        if 'phone' in missing_scopes and 'bindPhones' in first_detail:
            missing_scopes.remove('phone')

        assert not missing_scopes, f"缺少以下信息: {', '.join(missing_scopes)}"

        print("所有断言通过！测试成功")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求异常: {str(e)}\n建议检查VPN连接或网络配置")

    except AssertionError as e:
        # 添加详细错误信息
        error_msg = f"断言失败: {str(e)}"
        if 'response' in locals():
            error_msg += f"\n响应状态码: {response.status_code}"
            try:
                error_msg += f"\n响应内容: {response.text[:500]}"
            except:
                pass
        pytest.fail(error_msg)

    except Exception as e:
        pytest.fail(f"未处理的异常: {str(e)}")