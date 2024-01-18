from flask import Flask, render_template
import os
import markdown
from werkzeug.utils import secure_filename
import re

def safe_filename(filename):
    # Удалить небезопасные символы, но сохранить пробелы
    return re.sub(r'[^\w\s.-]', '', filename)

app = Flask(__name__)

def preprocess_markdown(markdown_content):
    # Replace '[x]' and '[ ]' with corresponding HTML elements for the task list
    markdown_content = markdown_content.replace('[x]', '<input type="checkbox" checked disabled>')
    markdown_content = markdown_content.replace('[ ]', '<input type="checkbox" disabled>')
    return markdown_content

def markdown_to_html(markdown_content):
    # Preprocess Markdown content
    markdown_content = preprocess_markdown(markdown_content)
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra', 'nl2br', 'sane_lists'])
    return html_content

def get_groups():
    groups = {}
    for group_name in os.listdir('posts'):
        group_path = os.path.join('posts', group_name)
        if os.path.isdir(group_path):
            groups[group_name] = []
            for filename in os.listdir(group_path):
                if filename.endswith('.md'):
                    path = os.path.join(group_path, filename)
                    with open(path, 'r') as file:
                        content = file.read()
                        lines = content.split('\n')
                        title = lines[0].replace('# ', '')
                        groups[group_name].append({'title': title, 'filename': filename})
    return groups

@app.route('/')
def index():
    groups = get_groups()
    return render_template('index.html', groups=groups)

@app.route('/posts/<group>/<filename>')
def post(group, filename):
    # Получение данных о группах и постах для меню
    groups = get_groups()

    # Загрузка и обработка выбранного поста
    group = safe_filename(group)  # Protect against path traversal attacks
    filename = safe_filename(filename)
    path = os.path.join('posts', group, filename)
    print(filename)
    if not os.path.exists(path):
        return f"File {filename} not found in group {group}.", 404

    # Если файл существует, продолжаем как обычно
    with open(path, 'r') as file:
        content = file.read()
        html_content = markdown_to_html(content)

    return render_template('post.html', content=html_content, groups=groups)


if __name__ == '__main__':
    app.run(debug=True)
