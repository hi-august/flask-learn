# coding=utf-8

import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

# 使用upload插件上传文件
from flask_uploads import UploadSet, configure_uploads, ALL

basedir = os.path.abspath(os.getcwd())

UPLOAD_FOLDER = os.path.join(basedir, 'upload')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 设置最大16m的上传文件


Files = UploadSet('files', ALL)
app.config['UPLOADS_DEFAULT_DEST'] = 'upload'
configure_uploads(app, Files)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['media']
        if file and allowed_file(file.filename):
            # secure_filename 过滤掉一些错误的路径
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))

    return render_template('upload.html')

# 使用upload插件
@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'media' in request.files:
        filename = Files.save(request.files['media'])
        url = Files.url(filename)
        print url
    return render_template('upload.html')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
