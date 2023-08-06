from .websocket_wrapper import *
import json
import requests

class hyperion_ng:

    led_reciever = None
    error_handeler = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        print(f'ws://{self.host}:{self.port}')
        self.__websocket = Websocket_wrapper(f'ws://{self.host}:{self.port}')
        if not self.__websocket.connect(): 
            return False
            
        self.__websocket.message_action = self.parse_message 
        # self.__websocket.set_on_close
        return True
        
    def disconnect(self):
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
        if not data or \
                data['command'] == "error" or \
                not data['command'] == 'ledcolors-ledstream-update':
            self.error_handeler(data)

        # parse led update command
        leds_data = self.parse_led_update(data)
        if self.led_reciever:
            self.led_reciever(leds_data)


    def parse_led_update(self, data):
        rawLedArr = data['result']['leds']

        leds_rgb = []

        i = 0
        while i < len(rawLedArr):
            leds_rgb.append(rawLedArr[i: i+3])
            i += 3

        return {
            'left': leds_rgb[2],
            'top': leds_rgb[0],
            'right': leds_rgb[1],
        }

    def __send_http_request(self, data):
        return requests.post(
            url=f'http://{self.host}:{self.port}/json-rpc', 
            data=data,
            ).json()

    def get_server_info(self):
        return self.__send_http_request('{"command":"serverinfo","tan":1}')



if __name__ == '__main__':

    def led_recieved(leds):
        print(leds)

    def err(err):
        print(f'error detected: {err}')

    hng = hyperion_ng('192.168.1.50',8090)
    hng.connect()
    hng.error_handeler = err
    hng.led_reciever = led_recieved
    
    hng.start_led_listener()

    sleep(5)
    
    hng.stop_led_listener()