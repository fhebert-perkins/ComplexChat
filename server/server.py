"""
Server Thing
"""

import logging
import asyncio
import websockets

CHANNELS = {}
HISTORY_LENGTH = 10
LOGGING_FORMAT = "%(asctime)s - %(message)s"

logging.basicConfig(format=LOGGING_FORMAT, filename="logging.log", level=logging.DEBUG)

async def handler(websocket, path):
    """Take and Echo to all who are connected"""

    path = path.split("/")[1]
    if path == '':
        path = "root"

    try:
        CHANNELS[path]["users"].append(websocket)
        logging.info("%s connected to #%s", websocket.remote_address, path)

    except KeyError:
        CHANNELS[path] = {"history":[]}
        CHANNELS[path]["users"] = []
        CHANNELS[path]["users"].append(websocket)
        logging.info("%s:%s created channel #%s",
                     websocket.remote_address[0],
                     websocket.remote_address[1],
                     path)

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
    logging.info("%s disconneced from #%s", websocket.remote_address, path)

START_SERVER = websockets.serve(handler, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
