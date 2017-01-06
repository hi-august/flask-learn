# coding=utf-8


from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('socketio.html')

# 接收消息
@socketio.on('my_event')
def my_event(message):
    print message, type(message)

# 发送消息
@socketio.on('my_response')
def custom_event(message):
    emit('my_response', {'data': 'send'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
