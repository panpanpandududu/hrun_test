from _pytest import config
from httprunner import HttpRunner,Config,Step,RunRequest,Parameters
import pytest

class TestregisterCasefail(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            {
                "user-psw-email": [
                    ["","123456","123@qq.com"], #注册账号为空
                    ["a","123456xxx","123@qq.com"],  #注册账号少于三个字符
                    ["aaaaaaabbbbbbbccccccc123233","","123@qq.com"], #注册账号大于30位字符
                    ["testx123","","123@qq.com"],   #密码为空
                    ["testx123","12345678912345678","123@qq.com"],  #密码大于16位，参数不合法，提示此字段不能超过16位
                    ["testx123","123456","123"],   #邮箱参数不合法，提示输入合法的邮箱地址
                    ["testx123","123","12@163.com"],   #密码少于3个，提示密码不得小于3位
                ]
            }
        ),
    )
    def test_start(self, param) :
        super().test_start(param)
    
    config = Config("注册失败用例参数化").base_url("${ENV(base_url)}")
    
    teststeps = [
        Step(
            RunRequest("step-注册")
            .post("/api/v1/register")
            .with_json({"username":"$user","password":"$psw","email":"$email"})
            .validate()
            .assert_equal("body.code",3003)
            .assert_equal("body.msg","参数不合法")
        )
    ]
