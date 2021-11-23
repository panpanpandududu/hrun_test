import pymysql

# 配置数据库信息
dbinfo = {
    "host": "49.235.92.12",
    "port": 3309,
    "user": "root",
    "password": "123456"}


class DbConnect(object):
    def __init__(self, db_cof, database=""):  # 构造函数
        # 打开数据库连接
        self.db = pymysql.connect(database=database,
                                  cursorclass=pymysql.cursors.DictCursor,  # 以字典的形式返回操作结果
                                  **db_cof)

        # 使用cursor()方法获取操作游标，以此方便对数据库的操作
        self.cursor = self.db.cursor()

    def select(self, sql):
        # SQL 查询语句
        # sql = "SELECT * FROM EMPLOYEE \
        #        WHERE INCOME > %s" % (1000)
        self.cursor.execute(sql)  # 使用execute()执行sql语句

        # fetchall()返回多个元组，即返回多条记录(rows),如果没有结果,则返回 ()
        # fetchone()返回单个的元组，也就是一条记录(row)，如果没有结果 , 则返回 None
        results = self.cursor.fetchall()
        return results

    def execute(self, sql):
        # SQL 删除、提交、修改语句
        # sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
        try:
            self.cursor.execute(sql)  # 执行SQL语句
            self.db.commit()  # 提交修改
        except:
            # 发生错误时回滚
            self.db.rollback()

    def close(self):
        # 关闭连接
        self.db.close()


if __name__ == '__main__':
    # 两个参数：数据库的配置信息（ip，端口，用户名，密码），数据库名
    db = DbConnect(dbinfo,  database="apps")
    # 查询
    sql1 = 'SELECT * FROM apiapp_goods WHERE id=1;'
    res1 = db.select(sql1)
    print(res1)

    # 执行
    sql2 = "UPDATE apiapp_goods SET goodsname='商品二' WHERE id=1"
    res2 = db.execute(sql2)
    res3 = db.select(sql1)
    print(res3)
    # sql2 = 'UPDATE apiapp_goods SET goodsname="xx悠悠课程" WHERE id=1;'
    # db.execute(sql2)
    # db.close()
