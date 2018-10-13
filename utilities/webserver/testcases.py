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
    asyncio.set_event_loop(asyncio.new_event_loop())
    server.start()

def webserver_sending():
    time.sleep(4)
    result = requests.get('http://localhost:8000/get_word_vector?word=中国')
    print(result.text)

    result = requests.post('http://localhost:8000/get_word_vector', data = json.dumps({'word': '中国'}))
    print(result.text)

    result = requests.get('http://localhost:8000/get_nearest_word_list?word=中国')
    print(result.text)

def testcases():
    webserver_listening_thread = threading.Thread(target = webserver_listening)
    webserver_sending_thread = threading.Thread(target = webserver_sending)

    webserver_listening_thread.start()
    webserver_sending_thread.start()

    webserver_listening_thread.join()
    webserver_sending_thread.join()

if __name__ == '__main__':
    testcases()
