#验证商品编码

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from httprunner import Config,Step,Parameters,RunRequest,HttpRunner,RunTestCase
import pytest
from testcase.login.login_success_test import TestCaseLoginSuccess as login

class TestCaseGoodsstatus(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            { 
                #商品状态只有0（下架），1（出售中），其他数字均失败
                "goodsstatus-code": [
                    [0,0],  #不能为空
                    [1,0],  #不少于8字符
                    [None,3003],  #必须以sp开头
                    [3,3003], #不能重复添加
                 ]
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)
    config = (
        Config("添加商品")
        .variables(
            **{
                "goodsname": "ceshi",
                "merchantid": "10001",
                "merchantname": "悠悠",
                "goodsprice": 99.9,
                "stock": 100,
                "goodsgroupid": 0,
                "goodsstatus": 1,
                "price": 21.0,
                "goodscode": "${goods_code()}",
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
           
        )
    ]