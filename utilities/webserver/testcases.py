import threading
import time
import asyncio
import json
import requests

from utilities.logger import Logger
from utilities.webserver import Server
from utilities.configuration import Configuration

def webserver_listening():
    logger = Logger(
        main_title = 'webserver',
        flow_type = 'test'
    )
    configuration = Configuration('./config/services.json')
    server = Server(configuration = configuration, logger = logger, port = 8000)
    server.start()

def webserver_sending():
    time.sleep(2)
    result = requests.post('http://localhost:8000/print', data = json.dumps({'text': '12345'}))
    print(result.text)

    result = requests.get('http://localhost:8000/add?x=3&y=4')
    print(result.text)

    result = requests.post('http://localhost:8000/add', data = json.dumps({'x': 1, 'y': '3'}))
    print(result.text)

    result = requests.get('http://localhost:8000/add?a=3&b=4')
    print(result)

    result = requests.post('http://localhost:8000/add', data = json.dumps({'a': 1, 'b': '3'}))
    print(result)

def testcases():
    webserver_listening_thread = threading.Thread(target = webserver_listening)
    webserver_sending_thread = threading.Thread(target = webserver_sending)

    webserver_listening_thread.start()
    webserver_sending_thread.start()

    webserver_listening_thread.join()
    webserver_sending_thread.join()

if __name__ == '__main__':
    webserver_listening()
