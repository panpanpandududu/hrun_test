# NOTE: Generated By HttpRunner v3.1.6
# FROM: testcase/part1/login_sign.yml


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCaseLoginSign(HttpRunner):

    config = (
        Config("登录签名sign测试用例")
        .variables(**{"user": "test1", "psw": "123456x"})
        .base_url("http://49.235.92.12:8201")
    )

    teststeps = [
        Step(
            RunRequest("sign测试用例")
            .setup_hook("${setup_hook()}")
            .setup_hook("${get_sign($request)}")
            .post("/api/v1/login")
            .with_json(
                {
                    "account": "$user",
                    "captcha": "$psw",
                    "password": "xxxx",
                    "uuid": None,
                }
            )
            .teardown_hook("${teardown_hook()}")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.msg", "login success!")
            .assert_equal("body.code", 0)
            .assert_equal("body.username", "$user")
        ),
    ]


if __name__ == "__main__":
    TestCaseLoginSign().test_start()