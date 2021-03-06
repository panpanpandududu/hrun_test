# NOTE: Generated By HttpRunner v3.1.6
# FROM: testcase/part1/update_info.yml


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


import pytest
from httprunner import Parameters


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase

from testcase.part1.login_test import TestCaseLogin as Login


class TestCaseUpdateInfo(HttpRunner):
    @pytest.mark.parametrize(
        "param", Parameters({"user-psw": "${P(data/user_psw.csv)}"})
    )
    def test_start(self, param):
        super().test_start(param)

    config = Config("修改个人信息").base_url("http://49.235.92.12:8201")

    teststeps = [
        Step(RunTestCase("step1-login").call(Login).export(*["token"])),
        Step(
            RunRequest("step2- update info")
            .post("/api/v1/userinfo")
            .with_headers(**{"Authorization": "Token $token"})
            .with_json(
                {"name": "$user", "sex": "M", "age": 20, "mail": "283340479@qq.com"}
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.code", 0)
        ),
    ]


if __name__ == "__main__":
    TestCaseUpdateInfo().test_start()
