import os
import re
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from blog_utils import markdown_utils
import configparser



app = Flask(__name__)
app.secret_key = 'aaa111'  # 设置一个秘密密钥

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 在此处添加您的验证逻辑，以下是示例
        if username == 'admin' and password == 'password':
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/edit_post', methods=['GET', 'POST'])
@app.route('/edit_post/<string:title>', methods=['GET', 'POST'])
@login_required
def edit_post(title=None):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_post(title, content)
        return redirect(url_for('index'))
    else:
        content = ""
        if title:
            try:
                with open(os.path.join('blog', f'{title}.md'), 'r') as file:
                    content = file.read()
            except FileNotFoundError:
                content = ""
        return render_template('edit_post.html', title=title, content=content)

@app.route('/upload_post', methods=['POST'])
def upload_post():
    file = request.files['markdown_file']
    if file:
        # 获取文件名
        filename = file.filename

        # 检查文件名是否包含中文
        if re.search("[\u4e00-\u9FFF]", filename):
            # 包含中文，保持原始文件名
            filename = filename.encode('utf-8').decode('utf-8')
        else:
            # 不包含中文，使用安全的文件名
            filename = secure_filename(filename)

        # 保存文件的目录
        upload_folder = 'blog'

        # 确保目录存在
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 文件的完整路径
        filepath = os.path.join(upload_folder, filename)

        # 保存文件
        file.save(filepath)

        return 'File uploaded successfully'
    return 'No file uploaded'

def save_post(title, content):
    if not os.path.exists('blog'):
        os.makedirs('blog')
    with open(os.path.join('blog', f'{title}.md'), 'w') as file:
        file.write(content)

@app.route('/')
def index():
    posts = markdown_utils.generate_blog_posts('blog')
    return render_template('index.html', posts=posts)


@app.route('/post/<string:title>')
def post(title):
    posts = markdown_utils.generate_blog_posts('blog')
    # 筛选出非目录的帖子，并匹配标题
    post = next((p for p in posts if p['title'] == title and not p.get('is_directory', False)), None)
    if post:
        return render_template('post.html', post=post)
    else:
        return 'Post not found', 404


config = configparser.ConfigParser()
config.read('config.ini')
flask_config = config['flask']
debug = flask_config.getboolean('debug')
host = flask_config.get('host')
port = flask_config.getint('port')
if __name__ == '__main__':
    app.run(debug=debug, host=host, port=port)
