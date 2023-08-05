import json
import threading
import time
from typing import Callable, Any

import websocket

from .util import new_id

EVENT_NAME = 'name'
EVENT_DATA = 'data'
EVENT_ADD_TARGET = 'add_target'


class Stream:

    def __init__(self, client, url):
        self.client = client
        self.url = url

        self.__hooks = {}
        self.__thread = None
        self.__websocket = None

    def start(self):
        def on_open(ws):
            self.__websocket = ws

        def on_error(ws, *args):
            print('ws err', *args)

        def on_close(ws, *args):
            print('ws close', *args)

        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.__on_message,
            on_open=on_open,
            on_error=on_error,
            on_close=on_close,
        )
        self.__thread = threading.Thread(target=ws.run_forever, args=())
        self.__thread.start()
        wait = 0.01
        while True:
            if self.__websocket is not None:
                return
            time.sleep(wait)
            wait *= 2

    def join(self):
        self.__thread.join()

    def subscribe(self, obj_id, event, cb, specials=True, payload=False):
        id = new_id()

        sub = {}

        sub['messageId'] = id
        sub['referenceId'] = '00000000000000000000000000000000'
        sub['command'] = 'subscribe'

        sub['object'] = obj_id
        sub['event'] = event
        sub['specials'] = specials
        sub['payload'] = payload

        self.__hooks[id] = cb

        self.__websocket.send(json.dumps(sub))

        return id

    def __on_message(self, ws, msg):
        msg = json.loads(msg)

        ref = msg['referenceId']

        cb = self.__hooks.get(ref)
        if cb is None:
            return

        cb(msg['event'])
