"""
Server Thing
"""

import asyncio
import websockets

# async def consumer(message, path, ws):
#     """Process and send message to all who listen"""
#     ws.send(message)

CHANNELS = {}
HISTORY_LENGTH = 10

async def handler(websocket, path):
    """Take and Echo to all who are connected"""
    try:
        CHANNELS[path]["users"].append(websocket)
        print("Connected", path)
    except KeyError:
        CHANNELS[path] = {"history":[]}
        CHANNELS[path]["users"] = []
        CHANNELS[path]["users"].append(websocket)
    if len(CHANNELS[path]["history"]) > 0:
        for msg in CHANNELS[path]["history"]:
            await websocket.send(msg)
    try:
        while True: # while connection open...
            message = await websocket.recv()

            CHANNELS[path]["history"].append(message)

            if len(CHANNELS[path]["history"]) > HISTORY_LENGTH:
                CHANNELS[path]["history"].pop(0)

            if message != "":
                for user in CHANNELS[path]["users"]:
                    await user.send(message)
    except websockets.exceptions.ConnectionClosed:
        CHANNELS[path]["users"].remove(websocket)
        print("disconnect")

START_SERVER = websockets.serve(handler, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
