负责网站后台和爬虫, 还有一些验证码识别

网站主要是以flask框架,前端是bootstrap来布局页面,mongo为存储
用到了flask_login插件来处理登陆模块
flask_admin来管理后台数据
celery作为分布式任务队列以处理后台任务
redis来缓存后台数据,以减少服务器压力

爬虫主要是用scrapy框架爬取,用beautifulsoup来提取网页内容
做过一些功能, 去重,编码检测,随机user-agent,mongo存储中间件,
本地代理ip,开启gzip,开启dns缓存
遇到js的话,用的是phantomjs处理js渲染的网页
scrapy-redis实现分布式爬取
验证码识别, 主要是tesseract训练数据,来预测并识别验证码

爬虫防止被墙
设置延迟下载
设置user-agent
禁用cookies
代理ip
