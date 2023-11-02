import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api
from waitress import serve
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append('c:\\work\\stable-diffusion\\stable_diffusion_webui')

from config.config import ServerConfig
from controller.db_controller import DBConn
 
# 서버 관련 config
scfg = ServerConfig()

# Flask
app = Flask(__name__)
api = Api(app)

# 세션을 위한 시크릿 키 설정
app.secret_key = 'your_secret_key'  
app.debug = scfg.debug

# 현재 스크립트의 디렉토리 경로를 가져옵니다.
basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 사용자 정보 검증 로직 (DB 조회 등) 추가
        user = {'email': email, 'password': password}
        
        if user:
            flash('로그인 성공!', 'success')
            
            # webui_main 함수를 새로운 터미널에서 실행
            current_directory = os.path.dirname(os.path.abspath(__file__))
            webui_path = os.path.join(current_directory, 'webui.py')
            subprocess.Popen(["python", webui_path])
            
            return redirect(url_for('home'))
        else:
            flash('로그인 실패! 이메일 또는 비밀번호를 확인하세요.', 'danger')
    return render_template('login.html')

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
