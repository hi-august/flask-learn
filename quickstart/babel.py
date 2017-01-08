#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template
# todo import error
from flask.ext.babel import Babel, gettext as _



app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    day = 'Saturday'
    return render_template('index.html', day=day)

if __name__ == '__main__':
    app.run()
