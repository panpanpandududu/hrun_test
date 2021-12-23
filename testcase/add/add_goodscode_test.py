#验证商品编码

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from httprunner import Config,Step,Parameters,RunRequest,HttpRunner,RunTestCase
import pytest
from testcase.login.login_success_test import TestCaseLoginSuccess as login

class TestCaseGoodscode(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            {
                "goodsname-goodscode-code-msg": [
                    ["yoyo123","",2000,"缺少必填项goodscode"],  #不能为空
                    ["yoyo123","spyo123",3003,"参数不合法"],  #不少于8字符
                    ["yoyo123","yoyo123xx",3003,"参数不合法"],  #必须以sp开头
                    ["yoyo123","sp_10086",4000,"goodscode不能重复添加"], #不能重复添加
                    ["yoyo123","sp1aaaaaaaaaaxxxdddwwwwfggg",3003,"参数不合法"]  #不能超过30字符
                 ]
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)
    config = (
        Config("添加商品不成功-goodscode异常")
        .variables(
            **{
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
            .assert_equal("body.code","$code" )
            .assert_equal("body.msg","$msg")
        )
    ]