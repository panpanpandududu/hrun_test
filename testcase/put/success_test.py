import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase

from testcase.login.login_success_test import TestCaseLoginSuccess as LoginSuccess


class TestCasePutGoodssuccess(HttpRunner):

    config = Config("修改接口商品ID是否正确").base_url("${ENV(base_url)}").variables(**{
        "id": 1
    })

    teststeps = [
        Step(RunTestCase("step1").call(LoginSuccess).export(*["token"])),
        Step(
            RunRequest("step2")
            .put("/api/v2/goods/$id")
            .with_headers(**{"Authorization": "Token $token"})
            .with_json(
                {
                    "goodsname": "pan",
                    "goodscode": "sp_test1",
                    "merchantid": "10001",
                    "goodsprice": 99.9,
                    "stock": 100,
                    "goodsgroupid": 0,
                    "goodsstatus": 1,
                    "price": 21.0,
                }
            )
            .validate()
            .assert_equal("body.code", 0)
        ),
    ]