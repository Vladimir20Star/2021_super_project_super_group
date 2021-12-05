import socket

sock = socket.socket()
sock.bind(('', 16363))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024)
    print(type(data), data)
    if not data:
        break
    conn.send(data.upper())

conn.close()
