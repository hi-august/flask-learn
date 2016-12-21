# coding=utf-8

from app.models import Jianshu

# $project需要输出的字段
# $match匹配到符合条件
# $skip过滤(跳过前面几个)
ret = Jianshu.objects.aggregate([
])
for x in ret:
    print x
