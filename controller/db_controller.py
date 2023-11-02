from config.config import ServerConfig, DBConfig
import pymysql

# 서버 관련 config
scfg = ServerConfig()
# DB 관련 config
dbcfg = DBConfig()

class DBConn:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.db_config.mysql_host,
                port=self.db_config.mysql_port,
                user=self.db_config.mysql_user,
                password=self.db_config.mysql_pwd,
                database=self.db_config.mysql_db,
                charset="utf8"
            )
            print("데이터베이스 연결 성공.")
        except Exception as e:
            print(f"데이터베이스 연결 오류: {e}")
            self.conn = None

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        self.close()

    def insert(self, name, email, password):
        with self.conn.cursor() as cur:
            query = f"INSERT INTO {self.db_config.mysql_table} (name, email, password) VALUES (%s, %s, %s)"
            cur.execute(query, (name, email, password))
            self.conn.commit()

    def get_data(self, email, password):
        with self.conn.cursor() as cur:
            query = f"SELECT * FROM {self.db_config.mysql_table} WHERE email = %s AND password = %s"
            cur.execute(query, (email, password))
            user = cur.fetchone()
        return user

    def get_user_by_email(self, email):
        if self.conn is None:
            print("데이터베이스 연결이 설정되지 않았습니다.")
            return None

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cur:
                query = f"SELECT * FROM {self.db_config.mysql_table} WHERE email = %s"
                cur.execute(query, (email,))
                user = cur.fetchone()
            return user
        except Exception as e:
            print(f"이메일로 사용자를 가져오는 중 오류 발생: {e}")
            return None