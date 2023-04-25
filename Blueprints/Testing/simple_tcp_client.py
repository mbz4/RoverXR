import socket

'''
TCP CLIENT ON LAPTOP
'''

# host = '192.168.199.29'
host = 'localhost'
port = 3333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Connecting...\nhost: {host}\nport: {port}")
s.connect((host, port))
s.sendall(b"Hello, world")
data = s.recv(1024)
print(f"Received:\n{repr(data)}")
s.close()