import pytest
import pytest_html
from py.xml import html




def pytest_configure(config):
    # 兼容旧版本的元数据设置
    if not hasattr(config, '_metadata'):
        config._metadata = {}
    config._metadata["项目名称"] = "电商自动化"
    config._metadata["测试环境"] = "UAT环境"

    # 删除不需要的默认元数据
    for key in ["Packages", "Plugins"]:
        if key in config._metadata:
            del config._metadata[key]


# 添加自定义内容到报告
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        html.h2("测试概览"),
        html.p("本次测试覆盖了核心交易流程"),
        html.h2("自定义分析图表"),
        html.img(src="chart.png", style="width:80%"),
    ])


# 添加失败截图（可选）
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        # 这里添加截图逻辑
        html_content = '<div>失败截图占位</div>'
        report.extra = [pytest_html.extras.html(html_content)]
