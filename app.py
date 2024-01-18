from flask import Flask, render_template
import os
import markdown

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

app = Flask(__name__)

@app.route('/')
def index():
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
    return render_template('index.html', groups=groups)

@app.route('/posts/<group>/<filename>')
def post(group, filename):
    path = os.path.join('posts', group, filename)
    with open(path, 'r') as file:
        content = file.read()
        html_content = markdown_to_html(content)
    return render_template('post.html', content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
