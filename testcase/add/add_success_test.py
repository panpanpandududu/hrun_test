import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from httprunner import Config,Step,Parameters,RunRequest,HttpRunner,RunTestCase
import pytest
from testcase.login.login_success_test import TestCaseLoginSuccess as login

class TestAddCase(HttpRunner):
    # @pytest.mark.parametrize(
    #     "param",
    #     Parameters(
    #         {
    #             "merchantid": ["",]
    #         }
    #     )
    # )
    config = (
        Config("添加商品成功")
        .variables(
            **{
                "goodsname": "yoyo",
                "goodscode": "${goods_code()}",
                "merchantid": "10001",
                "merchantname": "悠悠",
                "goodsprice": 99.9,
                "stock": 100,
                "goodsgroupid": 0,
                "goodsstatus": 1,
                "price": 21.0,
            }
        )
        .base_url("${ENV(base_url)}")
    )

    teststeps = [
        Step(RunTestCase("step1-login").call(login).export(*["token"])),
        Step(
            RunRequest("添加商品")
            .post("/api/v2/goods")
            .with_headers(**{"Authorization":"Token $token"})
            .with_json(
                {
                    "goodsname": "$goodsname",
                    "goodscode": "$goodscode",
                    "merchantid": "$merchantid",
                    "merchantname": "$merchantname",
                    "goodsprice": "$goodsprice",
                    "stock": "$stock",
                    "goodsgroupid": "$goodsgroupid",
                    "goodsstatus": "$goodsstatus",
                    "price": "$price",
                }
            )
            .validate()
            .assert_equal("body.code",0)
            .assert_equal("body.msg","success!")
        )
    ]