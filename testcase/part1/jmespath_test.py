import jmespath

body ={
    "code":0,
    "msg": "成功success！",
    "data":[
        {
            "age":20,
            "createtime": "2019-09-15",
            "id":1,
            "mail": "1378190284@qq.com",
            "name": "panpan",
            "sex": "nv"
        },
        {
            "age":22,
            "createtime": "2019-09-15",
            "id":2,
            "mail": "13820871007@qq.com",
            "name": "pan",
            "sex": "nv"
        }
    ]

}
#提取code
code = jmespath.search("code",body)
print(code)
#提取data数据
data = jmespath.search("data",body)
print(data)
#提取data中的第一条数据
data_first = jmespath.search('data[0]',body)
print(data_first)  #{'age': 20, 'createtime': '2019-09-15', 'id': 1, 'mail': '1378190284@qq.com', 'name': 'panpan', 'sex': 'nv'}
#提取data数据中name的值为pan的邮箱
email = jmespath.search("data[?name=='pan'].mail",body)
print(email)  #['13820871007@qq.com']  这是个列表
mail = jmespath.search("data[?name=='pan'].mail|[0]",body)
print(mail)  #13820871007@qq.com

#提取年龄大于21的个数
age_num = jmespath.search("data[?age>`21`]",body)
print(age_num)



