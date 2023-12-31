import markdown2
import os

def generate_blog_posts(blog_dir):
    posts = []
    for filename in os.listdir(blog_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(blog_dir, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                html_content = markdown2.markdown(content)
                post = {
                    'title': filename.replace('.md', ''),  # 或者提取文件中的标题
                    'content': html_content
                }
                posts.append(post)
    return posts



def generate_static_pages(blog_dir, output_dir):
    """
    从指定目录读取 Markdown 文件，转换为 HTML，并保存为静态文件。
    :param blog_dir: 存放 Markdown 文件的目录
    :param output_dir: 存放生成的静态 HTML 文件的目录
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    posts = generate_blog_posts(blog_dir)
    for i, post in enumerate(posts):
        html_page = f'''
        <!doctype html>
        <html>
        <head>
            <title>Post {i+1}</title>
            <style>
                /* Your CSS styles */
            </style>
        </head>
        <body>
            <div class="container">{post}</div>
        </body>
        </html>
        '''
        output_filepath = os.path.join(output_dir, f'post_{i+1}.html')
        with open(output_filepath, 'w') as output_file:
            output_file.write(html_page)
