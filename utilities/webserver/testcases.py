import threading
import time
import asyncio
import json
import requests

from constants import METHOD
from utilities.webserver import Application

def testcases():
    def webserver_listening():
        def add(x, y = '1'):
            x = int(x)
            y = int(y)
            return str(x + y)

        def print(text):
            return text

        application = Application()
        application.regist_service(add, api_path = '/add', method_list = [METHOD.GET, METHOD.POST])
        application.regist_service(print, api_path = '/print', method_list = [METHOD.POST])
        asyncio.set_event_loop(asyncio.new_event_loop())
        application.start(port = 8000)

    def webserver_testing():
        time.sleep(2)
        result = requests.post('http://localhost:8000/print', data = json.dumps({'text': '12345'}))
        print(result.text)

        result = requests.get('http://localhost:8000/add?x=3&y=4')
        print(result.text)

        result = requests.post('http://localhost:8000/add', data = json.dumps({'x': 1, 'y': '3'}))
        print(result.text)

    webserver_listening_thread = threading.Thread(target = webserver_listening)
    webserver_listening_thread.start()
    webserver_testing_thread = threading.Thread(target = webserver_testing)
    webserver_testing_thread.start()

    webserver_listening_thread.join()
    webserver_testing_thread.join()

if __name__ == '__main__':
    testcases()

