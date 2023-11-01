from config.config import ServerConfig, DBConfig
import pymysql

# 서버 관련 config
scfg = ServerConfig()
# DB 관련 config
dbcfg = DBConfig()

class DBConn:
    def __init__(self):
        try:
            self.host = dbcfg.mysql_host
            self.port = dbcfg.mysql_port
            self.user = dbcfg.mysql_user
            self.password = dbcfg.mysql_pwd 
            self.database = dbcfg.mysql_db
            self.charset="utf8"
            self.conn = pymysql.connect(host=self.host, port =self.port, user=self.user, password=self.password, database=self.database)
        except Exception as e:
            print('접속오류', e)

    def insert(self, name, email, password):
        cur = self.conn.cursor()
        query = f"INSERT INTO {dbcfg.mysql_table} (name, email, password) VALUES ('{name}', '{email}', '{password}')"
        cur.execute(query)
        self.conn.commit()
        cur.close()
        self.conn.close()

        
    def get_data(self, email, password):
        cur = self.conn.cursor()
        query = f"SELECT * FROM {dbcfg.mysql_table} WHERE email = '{email}' AND password = '{password}'"
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        self.conn.close()
        return user