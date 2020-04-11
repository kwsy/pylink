import pymysql


class Connect_Mysql:
    def __init__(self):
        self.host = '101.201.225.172'
        self.user = 'hjfdata'
        self.pwd = '123456!'
        self.port = '3309'
        self.db = 'hjf_pylink'

    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(self.host, self.user,
                           self.pwd, self.db, charset='utf8')
        except:
            print("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

def test():
    sql = """select * from csdn_hjf;"""

    cursor = Connect_Mysql.mysqlDB().cursor()
    cursor.execute(sql)
    cursor.close()


if __name__ == '__main__':
    test()