import pymysql
import yaml
from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키 설정

# 현재 스크립트의 디렉토리 경로를 가져옵니다.
basedir = os.path.abspath(os.path.dirname(__file__))

# db.yaml 파일의 경로를 설정합니다.
db_config_path = os.path.join(basedir, 'db.yaml')

# db.yaml 파일을 엽니다.
with open(db_config_path, 'r') as f:
    db = yaml.safe_load(f)

# 데이터베이스 연결 설정
app.config['MYSQL_HOST'] = db.get('mysql_host', 'localhost')
app.config['MYSQL_USER'] = db.get('mysql_user', 'root')
app.config['MYSQL_PASSWORD'] = db.get('mysql_password', '1234')
app.config['MYSQL_DB'] = db.get('mysql_db', 'test')

# 데이터베이스 연결 함수
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            flash('로그인 성공!', 'success')
            return redirect(url_for('home'))
        else:
            flash('로그인 실패! 이메일 또는 비밀번호를 확인하세요.', 'danger')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('회원가입 성공! 로그인하세요.', 'success')
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
