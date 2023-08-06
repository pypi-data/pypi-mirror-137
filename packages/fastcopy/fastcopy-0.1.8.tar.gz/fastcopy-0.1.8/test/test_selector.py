import socket
from selectors import DefaultSelector, EVENT_READ

a, b = socket.socketpair()
b.settimeout(0.001)

c, d = socket.socketpair()
d.settimeout(0.001)

e, f = socket.socketpair()
f.settimeout(0.001)

s = DefaultSelector()
s.register(b, EVENT_READ)
s.register(d, EVENT_READ)
s.register(f, EVENT_READ)


for k, _ in s.select():
    try:
        data = k.fileobj.recv(10, socket.MSG_WAITALL)
        print(k.fd, data)
    except Exception as err:
        print(k.fd, err)
