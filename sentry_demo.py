# coding=utf-8

from raven import Client

c = Client('http://39aeb386bf7842a6b92dd93ff81eb998:c2085725a8b74bdfa8df0e84001c7e1e@127.0.0.1:9000/2')

# 发送捕捉的消息, Exception
c.captureMessage('23333')

try:
    1/0
except ZeroDivisionError:
    ident = c.get_ident(c.captureException())
    print "Exception caught; reference is %s" % ident
