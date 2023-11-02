import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_restful import Api
from waitress import serve
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append('c:\\work\\stable-diffusion\\stable_diffusion_webui')

from config.config import ServerConfig, DBConfig
from controller.db_controller import DBConn
 
# 서버 관련 config
scfg = ServerConfig()
# DB 관련 config
dbcfg = DBConfig()  # DBConfig 인스턴스 생성


# Flask
app = Flask(__name__)
api = Api(app)

# 세션을 위한 시크릿 키 설정
app.secret_key = 'your_secret_key'  
app.debug = scfg.debug

# 현재 스크립트의 디렉토리 경로를 가져옵니다.
basedir = os.path.abspath(os.path.dirname(__file__))
current_directory = os.path.dirname(os.path.abspath(__file__))

# webui.py를 실행합니다.
webui_path = os.path.join(current_directory, 'webui.py')
subprocess.Popen(["python", webui_path])

@app.route('/')
def home():
    return render_template('index.html')

def is_logged_in():
    return 'logged_in' in session and session['logged_in']

@app.route('/webui')
def webui():
    if not is_logged_in():
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('login'))
    return redirect('http://localhost:7860')  # 여기서 webui.py가 실행되는 포트입니다. 필요에 따라 변경하세요.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = DBConn(dbcfg)
        user = conn.get_user_by_email(email)

        if user and user['password'] == password:
            flash('로그인 성공!', 'success')
            session['logged_in'] = True
            session['email'] = email
            g.user_email = email
            return redirect(url_for('webui'))
        else:
            flash('로그인 실패! 이메일 또는 비밀번호를 확인하세요.', 'danger')
            return render_template('index.html')
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = DBConn()
        conn.insert(name, email, password)

        flash('회원가입 성공! 로그인하세요.', 'success')
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    serve(app, host=scfg.host, port=scfg.port)
