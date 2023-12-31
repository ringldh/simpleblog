from flask import Flask, render_template
from butils import markdown_utils


app = Flask(__name__)

@app.route('/')
def index():
    posts = markdown_utils.generate_blog_posts('blog')
    return render_template('index.html', posts=posts)

@app.route('/posts/<string:title>')
def post(title):
    posts = markdown_utils.generate_blog_posts('blog')
    post = next((p for p in posts if p['title'] == title), None)
    if post:
        return render_template('post.html', post=post)
    else:
        return 'Post not found', 404

if __name__ == '__main__':
    app.run(debug=True)
