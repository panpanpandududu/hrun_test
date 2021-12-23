from httprunner import HttpRunner,Config,Step,RunRequest

class TestgetgoodsCase(HttpRunner):
    config = (
            Config("查询商品信息")
            .base_url("http://49.235.92.12:8201")
            )
    
    teststeps = [
        # Step(
        #     RunRequest("查询商品-step")
        #     .get("/api/v1/goods")
        #     .with_params(**{"page":1, "size":2})
        #     .validate()
        #     .assert_equal("body.code",0)
        # )
        Step(
            RunRequest("post传参data类型")
            .post("/api/v4/login")
            .with_data({"username":"test","password":"123456"})
            .validate()
            .assert_equal("status_code",200)
            .assert_equal("body.code",0)
        )
    ]

