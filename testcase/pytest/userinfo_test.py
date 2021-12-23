import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from httprunner import HttpRunner,Config,Step,RunRequest,RunTestCase
from testcase.pytest.login_test import TestLoginCase as login

class TestInfoCase(HttpRunner):
    config = (
            Config('用户信息')
            .base_url("http://49.235.92.12:8201")
            .variables(**{"user":"test"})
    )

    teststeps = [
        #引用某个用例时，需先导入这个用例
        Step(
            RunTestCase("先登录，获取token").call(login).export(*["token"])
        ),
        Step(
            RunRequest("用户信息")
            .post("/api/v1/userinfo")
            .with_headers(**{"Authorization": "Token $token"})
            .with_json(
                {"name": "$user", "sex": "M", "age": 20, "mail": "283340479@qq.com"}
            )
            .validate()
            .assert_equal("body.code",0)
            .assert_equal("body.message","update some data!")

        )
    ]
