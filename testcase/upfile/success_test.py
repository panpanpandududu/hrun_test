import pytest 
from httprunner import HttpRunner,Config,Step,RunRequest,Parameters

class TestCaseUpfile(HttpRunner):
    @pytest.mark.parametrize(
        "param",
        Parameters(
            {
                "filepath-titlename-code-msg":[
                   ["data/pic.jpg","pan",0,"success!"],
                   ["data/pic.jpg","panpan",0,"success!"],
                ]
            }
        ),
    )
    def test_start(self, param):
        super().test_start(param)
    
    config = (
        Config("上传成功")
        .base_url("${ENV(base_url)}")
    )

    teststeps = [
        Step(
            RunRequest("step")
            .post("/api/v1/upfile")
            .upload(**{
                "file": "$filepath",
                "title": "$titlename"
            })
            .validate()
            .assert_equal("body.code", "$code")
            .assert_equal("body.msg", "$msg")
        ),
    ]