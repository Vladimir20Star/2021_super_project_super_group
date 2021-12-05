import socket

sock = socket.socket()
sock.connect(('localhost', 16363))
string1 = "hello, world!"
sock.send(string1.encode("hello, world!"))

data = sock.recv(1024)
sock.close()

print(data)
