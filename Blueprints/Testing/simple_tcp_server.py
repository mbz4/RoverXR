import socket
host = '0.0.0.0'
port = 3333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print(f"Listening...\nhost: {host}\nport: {port}")
s.listen(1)
conn, addr = s.accept()
while True:
    print(f"Received connection from:\n\tAddress: {addr}\n\tConnection: {conn}")
    data = conn.recv(1024)
    if not data:
        break
    print(f"Received: \n{repr(data)}")
    conn.sendall(data)
conn.close()