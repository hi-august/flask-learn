# coding=utf-8

# socketio
# 应用场景
# 1. 实时分析, 服务端将数据推送给客户端,客服端可以实时图表,日志
# 2. 实时聊天, 通过namespace和room实现socket多路复用
# 3. 流式传输, 可以传输图片,视频,音频等二进制的传输
# 4. 文档合并, 运行多个用户同时编辑一个文件,并能看到其做出的修改

import hashlib
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    roomid = md5('1')
    return render_template('socketio.html', roomid=roomid)


# 监听my_event事件
@socketio.on('my_event')
def my_event(message):
    emit('my_response', {'data': message['data']}, broadcast=True)

@socketio.on('join')
def on_join(msg):
    join_room(msg['room'])
    emit('my_response', {'data': '%s am in %s' %(request.sid, msg['room'])}, broadcast=True)

@socketio.on('room_msg')
def send_room_message(msg):
    # print dir(request)
    # print request.cookies
    # print request.sid
    emit(
        'my_response',
        {'data': msg['data']},
        room=msg['room'],
         )

# 发送消息
# @socketio.on('my_response')
# def custom_event(message):
    # emit('my_response', {'data': message['data']}, broadcast=True)

def md5(msg):
    md5 = hashlib.md5(msg.encode('utf-8')).hexdigest()
    return md5

class TalkNamespace(Namespace):
    def on_talk_event(self, msg):
        emit(
            'response',
            {'data': msg['data']},
             )
    def on_join(self, msg):
        join_room()
        emit(
            'response',
            {'data': 'In room'},
        )
    pass

# 后端处理
# 由于在实际运行中，可能会有大量的room需要建立，通过class将room抽象出来会更方便
class ChatRoom(Namespace):
    def on_connect(self):
        print('client connected to room')

    def on_disconnect(self):
        print('client disconnected from room')
    # 自定义的事件，前边需要加上on_
    def on_chat(self, msg):
        print('running chat')
        print(msg)
        # 发送信息到response
        self.emit('response', {'data': msg}, include_self=True)
    def on_recv(self, data):
        self.emit('response', data['msg'])

# 监听message事件
@socketio.on('message')
def getMsg(sss):
    print sss
    room = sss['msg']
    newRoom = ChatRoom('/{}'.format(room))  # 通过制定的room生成对应的聊天频道
    socketio.on_namespace(newRoom)

if __name__ == '__main__':
    socketio.run(app, debug=True)
