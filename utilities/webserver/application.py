import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello word')

def make_app():
    return tornado.web.Application(
        [(r'/', MainHandler),]
    )

if __name__ == '__main__':
    application = make_app()
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()
