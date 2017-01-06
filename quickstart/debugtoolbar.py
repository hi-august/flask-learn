#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['DEBUG_TB_HOSTS'] = '127.0.0.1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
# app.config['DEBUG_TB_PANELS'] = (
    # 'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    # 'flask_debugtoolbar.panels.logger.LoggingPanel',
    # 'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    # # 'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel' # 分析探查数据
    # # 'flask_debugtoolbar.panels.route_list.RouteListDebugPanel' # 路由列表
    # 'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel' # 配置
    # 'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel' # 共享变量
# )

# 初始化debug bar
toolbar = DebugToolbarExtension(app)


@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
