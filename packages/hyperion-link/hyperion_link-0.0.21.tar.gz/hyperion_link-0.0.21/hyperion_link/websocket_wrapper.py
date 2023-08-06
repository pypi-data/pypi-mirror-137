from time import sleep

import asyncio
import websocket


class WebsocketWrapper:
    def __init__(self, url):
        self.url = url
        self.message_action = None
        self.on_closed = None
        self.on_opened = None
        self.ws = None

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    # setters
    def set_on_message(self, fnc):
        self.message_action = fnc

    def set_on_close(self, fnc):
        self.on_closed = fnc

    def set_on_open(self, fnc):
        self.on_opened = fnc

    def connect(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.__on_message,
            on_close=self.__on_close,
            on_open=self.__on_open,
        )

        # listen to messages on seperate thread to prevent the blocking
        # of the entire app

        self.loop.run_in_executor(None, ws.run_forever)
        self.ws = ws

        # try to connect 5 times
        conn_timeout = 5
        print(self.ws.sock)
        # return
        while not self.ws.sock.connected:
            sleep(1)
            conn_timeout -= 1

        # if we cant connect stop we clean up
        if not self.ws.sock.connected:
            self.__cleanup()

        return self.ws.sock.connect

    def send_msg(self, msg):
        self.ws.send(msg)
        print(f" send message: \n\n {msg}\n\n" + "-" * 10)

    def stop(self):
        print("### STOPPING WEBSOCKET CLIENT ###")
        self.__cleanup()
        print("### WEBSOCKET CLIENT STOPPED")

    def __cleanup(self):
        # stop websocket
        self.ws.keep_running = False
        self.ws.close()

        # stop thread

    def __on_open(self, ws):
        if self.message_action:
            self.on_opened()
        else:
            print("### CONNECTION OPENED ###")

    def __on_close(self, ws):
        if self.message_action:
            self.on_closed()
        else:
            print("### CONNECTION CLOSED ###")

    def __on_message(self, ws, message):

        if self.message_action is not None:
            self.message_action(ws, message)
        else:
            print(message)
