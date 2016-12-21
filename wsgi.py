#!/usr/bin/env python
# -*- coding:utf-8 *-*

# gunicorn启动用到
from app import setup_app

app = setup_app()
if __name__ == '__main__':
    app.run()
