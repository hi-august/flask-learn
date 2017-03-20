# flaskdemo
flask exercises

####
1. Flask依赖于两个外部库,werkzeug和jinjia2
werkzeug是一个wsgi工具包,作为一个web框架的底层库
jinjia2是一个功能齐全的模板引擎
2. RESTful api, 即(Resource Representational State Transfer)
2.1 每一个url代表一种资源
2.2 客服端和服务端传递资源
2.3 客户端通过http动词对服务器资源进行操作
2.4 简单说就是url来定位资源, 用HTTP动词(GET,POST,PUT,DELETE)来对资源进行操作
一般来说,GET获取资源,POST添加(也可以用来更新资源),PUT更新,DELETE删除资源
2.5 无状态,统一接口,表现层,分层系统,状态转变
3. WSGI(web server gateway interface), 是python语言来定义web服务器和web应用程序
的接口,它封装了http请求,解析http请求,发送http请求,响应等底层操作
4. Flask中分为请求上下文(Request,Session), 和应用上下文(g,current_app)
RequestContext, request请求对象,封装了请求(environ)内容
session, 根据请求的cookie,载入访问者信息
AppContext, g,处理请求时用作临时存储的对象
current_app,当前激活程序实例
current_app生命周期最长,只要当前实例app在运行,current_app就不会失效
request和g一次请求后就失效,只存在于请求发生时
5. Flask处理流程
    1. 创建上下文, flask会根据wsgi封装的请求等信息(environ,RequestContext,AppContext)
    2. 入栈, RequestContext push _request_ctx_stack里,请求发生时,request,session对象指向这个栈顶端
    AppContext push _app_ctx_stack里,请求发生时,g对象指向这个栈顶元素
    3. 请求分发, flask调用full_dispatch_request进行请求分发,
    full_dispatch_request会根据请求的url找到对应的视图函数,并生成响应
    4. 上下文对象出栈,http响应已经生成,不需要request和g这两个上下文对象,出栈
    5. 响应wsgi, 调用response对象

