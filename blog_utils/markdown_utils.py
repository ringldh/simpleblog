import markdown2
import os

def generate_blog_posts(blog_dir):
    posts = []
    directories = set()
    for root, dirs, files in os.walk(blog_dir):
        for d in dirs:
            dir_path = os.path.relpath(os.path.join(root, d), blog_dir)
            directories.add(dir_path)  # 收集目录路径
        for filename in files:
            if filename.endswith('.md'):
                relative_path = os.path.relpath(root, blog_dir)
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    content = file.read()
                    html_content = markdown2.markdown(content)
                    post = {
                        'title': filename.replace('.md', ''),
                        'content': html_content,
                        'relative_path': relative_path,  # 为帖子设置相对路径
                        'is_directory': False  # 标记为非目录项
                    }
                    posts.append(post)

    # 为收集到的每个目录添加一个目录项
    for dir_path in directories:
        posts.append({
            'title': os.path.basename(dir_path),  # 目录名
            'is_directory': True,  # 标记为目录项
            'relative_path': dir_path  # 为目录设置相对路径
        })

    # 返回按路径和类型排序的帖子列表
    def sort_key(post):
        path_parts = post.get('relative_path', '').split(os.sep)
        directory_order = 0 if post.get('is_directory', False) else 1
        return (*path_parts, directory_order, post.get('title', ''))
    
    return sorted(posts, key=sort_key)





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
