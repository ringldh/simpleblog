import markdown2
import os

def generate_blog_posts(blog_dir):
    posts = []
    for root, dirs, files in os.walk(blog_dir):
        for filename in files:
            if filename.endswith('.md'):
                # 获取文件的相对路径
                relative_path = os.path.relpath(root, blog_dir)
                # 如果不在根目录，则将目录和文件名合并为完整路径
                if relative_path != ".":
                    path = os.path.join(relative_path, filename.replace('.md', ''))
                else:
                    path = filename.replace('.md', '')

                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    content = file.read()
                    html_content = markdown2.markdown(content)
                    post = {
                        'title': filename.replace('.md', ''),
                        'content': html_content,
                        'relative_path': path
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
