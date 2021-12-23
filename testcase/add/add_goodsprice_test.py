#验证商品编码

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from httprunner import Config,Step,Parameters,RunRequest,HttpRunner,RunTestCase
import pytest
from testcase.login.login_success_test import TestCaseLoginSuccess as login

class TestCaseGoodsprice(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            {
                "goodsprice-code-msg": [
                    [19.101234,0,"success!"], #精确到小数点后几位
                    [19.10,0,"success!"],  #浮点数
                    [19,0,"success!"],  #整数
                    ["",3003,"参数不合法"],  #
                    [None,0,"success!"],  #none不指向任何对象，不分配内存空间
                 ]
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)
    config = (
        Config("添加商品-goodsprice测试")
        .variables(
            **{
                "goodsname":"yoyo123",
                "goodscode": "${goods_code()}",
                "merchantid": "10001",
                "merchantname": "悠悠",
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
            .assert_equal("body.code","$code" )
            .assert_equal("body.msg","$msg")
        )
    ]