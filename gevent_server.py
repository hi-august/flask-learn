from gevent.wsgi import WSGIServer
from app import setup_app

app = setup_app()

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
