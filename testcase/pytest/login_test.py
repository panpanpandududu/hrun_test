from httprunner import HttpRunner,Config,Step,RunRequest,RunTestCase
from httprunner.testcase import StepRefCase

# *表述接收的参数作为元组来处理 ，元组是不可变的 *[]
# **表示接收的参数作为字典来处理  **{}
#引用变量： $key     引用函数 ${fun()}

class TestLoginCase(HttpRunner):   #定义一个类继承httprunner
    #两个重要对象， config，teststeps
    #实例化config
    config = (
        Config("py登录测试用例")
               .base_url("http://49.235.92.12:8201")
               .variables(**{"user":"test", "psw":"123456"})
               .export(*["token"])
        )
    
    #实例化 teststeps
    teststeps = [
        Step(
            RunRequest("login")
            .post("/api/v1/login")
            .with_json({"username": "$user", "password": "$psw"})
            .extract()
            .with_jmespath("body.token", "token")
            .validate()
            .assert_equal("body.code", 0)
            .assert_equal("body.msg", "login success!")
            .assert_length_equal("body.token", 40)
            )
        ]
