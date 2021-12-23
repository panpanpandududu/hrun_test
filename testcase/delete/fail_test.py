import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from httprunner import Config,Step,RunRequest,RunTestCase,HttpRunner,Parameters

from testcase.login.login_success_test import TestCaseLoginSuccess as login

import pytest

class TestCaseDeletefail(HttpRunner):
    @pytest.mark.parametrize(
        "param", 
        Parameters(
            {
                "delete_id": ["", "123456", "abc"]}   #空，不存在的ID，非法ID
        ),
     )
    def test_start(self, param):
        super().test_start(param)

    config = (
        Config("删除商品失败")
        .base_url("${ENV(base_url)}")
    )

    teststeps = [
        Step(RunTestCase("step1-登录").call(login).export(*["token"])),
        Step(
            RunRequest("step3-删除商品")
            .delete("/api/v2/goods/$delete_id")
            .with_headers(**{"Authorization": "Token $token"})
            .validate()
            .assert_equal("status_code",200)
        )
    ]