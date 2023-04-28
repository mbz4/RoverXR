import socket
import asyncio
'''
TCP SERVER ON Raspberry Pi
'''

class EchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        received_data = data.decode()
        print(f'received_data: {received_data}\nraw_data: {data}')
        self.transport.write(data) # echo back the data
        if received_data == "close":
            print("closed the connection")
            # close the socket
            self.transport.close()

loop = asyncio.get_event_loop()
coro = loop.create_server(EchoServer, 'localhost', 5000)
server = loop.run_until_complete(coro)
print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()

# async def handle_echo(reader, writer):
#     data = await reader.read(100)
#     message = data.decode()
#     addr = writer.get_extra_info('peername')
#     print(f"Received {message!r} from {addr!r}")
#     print(f"Send: {message!r}")
#     writer.write(data)
#     #await writer.drain()
#     #print("Close the connection")
#     #writer.close()
#     #await writer.wait_closed()

# async def main():
#     server = await asyncio.start_server(
#         handle_echo, 'localhost', 5000)

#     addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
#     print(f'Serving on {addrs}')

#     async with server:
#         await server.serve_forever()

# asyncio.run(main())

# # host = '0.0.0.0'
# host = 'localhost'
# port = 3333
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((host, port))
# print(f"Listening...\nhost: {host}\nport: {port}")
# s.listen(1)
# conn, addr = s.accept()
# # conn.sendall("hello from server!".encode("utf-8"))
# while True:
#     print(f"Received connection from:\n\tAddress: {addr}\n\tConnection: {conn}")
#     data = conn.recv(1024)
#     if not data:
#         break
#     print(f"Received: \n{repr(data)}")
#     conn.sendall(data)
# conn.close()