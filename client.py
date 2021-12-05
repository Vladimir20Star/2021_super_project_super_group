import socket

sock = socket.socket()
sock.connect(('localhost', 16363))
sock.send(155)

data = sock.recv(1024)
sock.close()

print(data)
