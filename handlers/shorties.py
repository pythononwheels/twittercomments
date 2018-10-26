import tornado.ioloop
import tornado.web
from twittercomments.handlers.base import BaseHandler
from twittercomments.application import app

# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 

@app.add_route("/", pos=1)
class IndexdHandler(BaseHandler):
    def get(self, index=None):
        print(" Calling IndexHandler from handlers/shorties.py: parameter index: " + str(index))
        self.render("index.tmpl")

# this will be the last route since it has the lowest pos.
@app.add_route(".*", pos=0)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.error( template="404.tmpl", http_code=404  )

