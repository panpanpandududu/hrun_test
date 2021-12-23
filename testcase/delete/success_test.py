import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from httprunner import Config,Step,RunRequest,RunTestCase,HttpRunner

from testcase.login.login_success_test import TestCaseLoginSuccess as login

class TestCaseDeletesuccess(HttpRunner):
    config = (
        Config("删除商品成功")
        .base_url("${ENV(base_url)}")
        .variables(
            **{
                "goodsname": "test",
                "goodscode": "${goods_code()}",

            }
        )
    )

    teststeps = [
        Step(RunTestCase("step1-登录").call(login).export(*["token"])),
        Step(
            RunRequest("step2-添加商品")
            .post("/api/v2/goods")
            .with_headers(**{"Authorization": "Token $token"})
            .with_json({"goodscode":"$goodscode","goodsname": "$goodsname"})
            .extract()
            .with_jmespath("body.data.id","delete_id")
            .validate()
            .assert_equal("body.code",0)
            .assert_equal("body.msg", "success!")
        ),
        Step(
            RunRequest("step3-删除商品")
            .delete("/api/v2/goods/$delete_id")
            .with_headers(**{"Authorization": "Token $token"})
            .validate()
            .assert_equal("body.code",0)
        )
    ]