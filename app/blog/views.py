# coding=utf-8

from flask import jsonify, render_template, request
from app import access_log
from app.models import Post
from app.blog import blog
import math

def parse_page_data(qs):
    total = qs.count()
    params = request.values.to_dict()
    try:
        page = int(params.get("page"))
    except TypeError:
        page = 1
    if page < 1:
        page = 1
    page_size = int(params.get("page_size", 20))
    page_num = int(math.ceil(total*1.0/page_size))
    skip = (page-1)*page_size

    cur_range = range(max(1, page-8),  min(max(1, page-8)+16, page_num+1))
    return {
        "total": total,
        "page_size": page_size,         # 每页page_size条记录
        "page_count": page_num,         # 总共有page_num页
        "cur_page": page,               # 当前页
        "previous": max(0, page-1),
        "next": min(page+1, page_num),
        "items": qs[skip: skip+page_size],
        "range": cur_range,             # 分页按钮显示的范围
    }

@blog.route('/', methods=['GET'])
def index():
    return render_template('blog/index.html')

@blog.route('/api', methods=['GET'])
def blog_api():
    qset = {}
    posts = parse_page_data(Post.objects(**qset))
    access_log.info(posts)
    return jsonify({'result': posts})

@blog.route('/test', methods=['GET'])
def test():
    return jsonify({'ok': 1})
