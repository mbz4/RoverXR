from websockets.server import serve
import asyncio
'''
WS CLIENT ON LAPTOP
'''
async def echo(websocket):
    async for message in websocket:
        message = message.decode("utf-8")
        print(f"Message from client: {message}")
        await websocket.send(f"Received your message: {message}")

async def main():
    async with serve(echo, "localhost", 3333):
        print("Server started")
        await asyncio.Future()

asyncio.run(main())