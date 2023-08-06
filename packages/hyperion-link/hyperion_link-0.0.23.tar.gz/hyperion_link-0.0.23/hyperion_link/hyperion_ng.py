import json
import asyncio
import requests

from .websocket_wrapper import WebsocketWrapper


class HyperionNg:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.led_info = {'left': 3, 'top': 4, 'right': 1, 'bottom': 2}

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def led_reciever(self, leds):
        pass

    def error_handeler(self, err):
        pass

    def connect(self):
        print(f"ws://{self.host}:{self.port}")
        self.__websocket = WebsocketWrapper(f"ws://{self.host}:{self.port}")
        if not self.__websocket.connect():
            return False

        self.__websocket.message_action = self.parse_message
        # self.__websocket.set_on_close
        return True

    def disconnect(self):
        self.loop.close()
        self.__websocket.stop()

    def start_led_listener(self):
        self.__websocket.send_msg(
            '{"command":"ledcolors", "subcommand":"ledstream-start"}'
        )

    def stop_led_listener(self):
        self.__websocket.send_msg(
            '{"command":"ledcolors","subcommand":"ledstream-stop"}'
        )

    def parse_message(self, ws, message):

        data = json.loads(message)

        # check if there is anything different recieved then expected
        if (
            not data
            or data["command"] == "error"
            or not data["command"] == "ledcolors-ledstream-update"
        ):
            if self.error_handeler is not None:
                self.error_handeler(data)
        else:
            # parse led update command
            leds_data = self.parse_led_update(data)
            self.loop.run_in_executor(None, self.led_reciever(leds_data))

    def parse_led_update(self, data):
        rawLedArr = data["result"]["leds"]

        leds_rgb = []

        i = 0
        while i < len(rawLedArr):
            leds_rgb.append(rawLedArr[i : i + 3])
            i += 3

        led_data = {}

        leds_used = 0
        for i in ['top','right','bottom','left']:
            amount_leds = self.led_info[i]
            print('-'*25)
            print(i)
            print(amount_leds)
            print(leds_used)
            print(leds_rgb)
            print(leds_rgb[leds_used: leds_used + amount_leds //2])
            center_led = (amount_leds // 2) + leds_used

            led_data[i] = leds_rgb[center_led]

            leds_used += amount_leds 

        return led_data
        
        # return {
        #     "left": leds_rgb[3],
        #     "top": leds_rgb[0],
        #     "right": leds_rgb[1],
        #     "bottom": leds_rgb[2],
        # }

    def __send_http_request(self, data):
        return requests.post(
            url=f"http://{self.host}:{self.port}/json-rpc",
            data=data,
        ).json()

    def get_server_info(self):
        return self.__send_http_request('{"command":"serverinfo","tan":1}')
