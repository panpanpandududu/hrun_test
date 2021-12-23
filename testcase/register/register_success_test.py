from _pytest import config
from httprunner import HttpRunner,Config,Step,RunRequest,Parameters
import pytest

class TestregisterCasesuccess(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            {
                "user-psw-email": [
                    ["${register_user()}","123456",""],
                    ["${register_user()}","123456","123@qq.com"]
                ]
            }
        ),
    )
    def test_start(self, param) :
        super().test_start(param)
    
    config = Config("注册成功用例参数化").base_url("${ENV(base_url)}")
    
    teststeps = [
        Step(
            RunRequest("step-注册")
            .post("/api/v1/register")
            .with_json({"username":"$user","password":"$psw","email":"$email"})
            .validate()
            .assert_equal("body.code",0)
            .assert_equal("body.msg","register success!")
        )
    ]
