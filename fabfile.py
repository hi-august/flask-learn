#!/usr/bin/env python
# encoding: utf-8

# 使用fabric部署
from fabric.api import env
from fabric.operations import run
from fabric.context_managers import cd

SERVER_LIST = {
    'apple': '150.129.82.175:53387',
}

env.user = 'root'
env.hosts = SERVER_LIST.values()


def deploy(name=''):
    with cd('/root/web/flaskdemo'):
        # 拉代码
        run("git checkout master")
        run("git fetch")
        run("git merge origin/master")

        # 重启supervisor
        run("sudo supervisorctl restart %s" % name)


def deploy_all():
    with cd(''):
        run("git checkout master")
        run("git fetch")
        run("git merge origin/master")

        for name in ['dashboard',]:
            run("sudo supervisorctl restart %s" % name)



# from fabric.api import *

# # 使用远程命令的用户名
# env.user = 'appuser'
# # 执行命令的服务器
# env.hosts = ['server1.example.com', 'server2.example.com']

# def pack():
#     # 创建一个新的分发源，格式为 tar 压缩包
#     local('python setup.py sdist --formats=gztar', capture=False)

# def deploy():
#     # 定义分发版本的名称和版本号
#     dist = local('python setup.py --fullname', capture=True).strip()
#     # 把 tar 压缩包格式的源代码上传到服务器的临时文件夹
#     put('dist/%s.tar.gz' % dist, '/tmp/yourapplication.tar.gz')
#     # 创建一个用于解压缩的文件夹，并进入该文件夹
#     run('mkdir /tmp/yourapplication')
#     with cd('/tmp/yourapplication'):
#         run('tar xzf /tmp/yourapplication.tar.gz')
#         # 现在使用 virtual 环境的 Python 解释器来安装包
#         run('/var/www/yourapplication/env/bin/python setup.py install')
#     # 安装完成，删除文件夹
#     run('rm -rf /tmp/yourapplication /tmp/yourapplication.tar.gz')
#     # 最后 touch .wsgi 文件，让 mod_wsgi 触发应用重载
#     run('touch /var/www/yourapplication.wsgi')
