# coding=utf-8

from app import setup_app
from app.models import Jianshu
from app.blog.models import MysqlJianshu, save

app = setup_app()

with app.app_context():
    for x in Jianshu.objects.filter():
        p = MysqlJianshu(title=x.title, url=x.url, link_id=x.link_id)
        res = save(p)
        print res

# $project需要输出的字段
# $match匹配到符合条件
# $skip过滤(跳过前面几个)
# ret = Jianshu.objects.aggregate([
# ])
# for x in ret:
    # print x
