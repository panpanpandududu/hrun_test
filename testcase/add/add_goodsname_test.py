#姓名字段校验
#引用路径问题
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from httprunner import HttpRunner,Config,Step,RunRequest,RunTestCase,Parameters
import pytest
from testcase.login.login_success_test import TestCaseLoginSuccess as login

class TestCaseGoodsname(HttpRunner):
    @pytest.mark.parameters(
        "param",
        Parameters(
            {
                "goodsname-code-msg": [
                    ["qwertyuiofnvjvnjvnjvndjndjjjsdjfeji",3003,"参数不合法"],  #不允许超过30个字符
                    ["",3003,"参数不合法"], #不允许为空字符串
                    ["yoyo123123",0,"success!"], #正确传参
                ]
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)
    
    config = (
        Config("商品名验证")
        .base_url("${ENV(base_url)}")
        .variables(
            **{
                "goodscode": "${goods_code()}",
                "goodsprice": 19,
                "merchantid": "10001",
                "merchantname": "悠悠",
                "stock": 100,
                "goodsgroupid": 0,
                "goodsstatus": 1,
                "price": 21.0,
            }
        )
    )

    teststep = [
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
            .assert_equal("body.code","$code")
            .assert_equal("body.msg","$msg")
        )]


