import MySQLdb
from profilehooks import profile
from NT.common.log import MyLog
from NT.data.config_param import ConfigParam


class DB:
    """操作mysql数据库"""

    def __init__(self):
        """链接数据库"""
        try:
            self.log = MyLog.get_log().logger

            # 读取config.ini文件中的数据库配置信息
            config = ConfigParam()
            host = config.get_db("host")
            port = int(config.get_db("port"))
            user = config.get_db("user")
            password = config.get_db("password")
            db = config.get_db("db")

            print(host, port, user, password, db)

            # 创建链接
            self.connection = MySQLdb.connect(host=host, port=port, user=user, password=password, db=db,
                                              charset="utf8mb4")
            # 创建游标
            self.cursor = self.connection.cursor()
        except MySQLdb.OperationalError as e:
            self.log.error("mysql Error %r：%r" % (e.args[0], e.args[1]))

    def clear(self, table_name):
        """删除表"""
        real_sql = "delete from" + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    @profile(immediate=True)  # 耗时
    def insert(self, table_name, table_data):
        """插入sql语句"""
        # real_sql = "INSERT INTO " + table_name + " VALUES (" + str(table_data) + ");"
        # self.log.debug(real_sql)

        with self.cursor as cursor:
            # cursor.execute(real_sql)
            # self.connection.commit()

            real_sql = "select * from " + table_name + ";"
            self.cursor.execute(real_sql)
            all_data = cursor.fetchone()
            self.log.debug(all_data)
            all_data = cursor.fetchmany()
            self.log.debug(all_data)
            all_data = cursor.fetchmany(2)
            self.log.debug(all_data)
            all_data = cursor.fetchall()
            self.log.debug(all_data)

    def close(self):
        """关闭数据库"""
        self.connection.close()


if __name__ == "__main__":
    db = DB()
    table_name = "sign_event"
    data = "8,'红米', 2000, 1, '北京会展中心', '2016-08-20 00:25:42', '2016-08-20 00:25:42'"
    table_name2 = "sign_guest"
    data2 = "22,'ddefs', 18241444422, 'ddefs@mail.com', 0,'2016-08-20 00:25:42', 1"

    # db.clear(table_name)
    db.insert(table_name2, data2)
    db.close()
