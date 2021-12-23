from _pytest import config
from httprunner import HttpRunner,Config,Step,RunRequest,Parameters
import pytest

class TestregisterCaseagain(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            {
                "user-psw-email": [
                    ["test","123456",""], #注册账号为空
                    ["test1","123456",""],  #注册账号少于三个字符
                ]
            }
        ),
    )
    def test_start(self, param) :
        super().test_start(param)
    
    config = Config("重复注册用例参数化").base_url("${ENV(base_url)}")
    
    teststeps = [
        Step(
            RunRequest("step-注册")
            .post("/api/v1/register")
            .with_json({"username":"$user","password":"$psw","email":"$email"})
            .validate()
            .assert_equal("body.code",2000)
            #.assert_equal("body.msg","用户已被注册")
        )
    ]
