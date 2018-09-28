from constants import METHOD
from utilities.webserver import Application

def testcases():
    def add(x, y = '1'):
        x = int(x)
        y = int(y)
        return str(x + y)

    def print(text):
        return text

    application = Application()
    application.regist_service(add, api_path = '/add', method_list = [METHOD.GET])
    application.regist_service(print, api_path = '/print', method_list = [METHOD.POST])
    application.start(port = 8000)

if __name__ == '__main__':
    testcases()

