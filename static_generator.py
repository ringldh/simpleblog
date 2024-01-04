import blog_utils.markdown_utils as markdown_utils

def generate_static_pages():
    markdown_utils.generate_static_pages('blog', 'static_pages')

if __name__ == '__main__':
    generate_static_pages()
