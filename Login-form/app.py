import subprocess
import sys
import pkg_resources
import os
import platform
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'requirements.txt'))

if not os.path.isfile(requirements_path):
    raise FileNotFoundError(f"Could not find a requirements.txt file at {requirements_path}")

installed_packages = {pkg.key for pkg in pkg_resources.working_set}

# Read the requirements file and install the packages
def read_requirements(path):
    for encoding in ['utf-8-sig', 'utf-16']:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.readlines()
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError(f"Could not decode the requirements file with any of the specified encodings.")

lines = read_requirements(requirements_path)

for line in lines:
    package = line.strip()
    package_name = package.split('==')[0] if '==' in package else package
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package {package}. Error: {e}")


from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_restful import Api
from waitress import serve

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
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


try:
    if platform.system() == 'Windows':
        # Windows에서 .bat 파일 실행
        subprocess.Popen(["webui.bat"], cwd=current_directory, shell=True)
    else:
        # Unix 기반 OS에서 .sh 파일 실행
        subprocess.Popen(["sh", "webui.sh"], cwd=current_directory)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Error running script: {e}")



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
    return redirect('http://127.0.0.1:7860')  

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
    print(f"\n Running on http://{scfg.host}:{scfg.port}/ LOGIN-FORM \n")
    serve(app, host=scfg.host, port=scfg.port)
    