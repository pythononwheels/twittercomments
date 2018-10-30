import tornado.ioloop
import tornado.web
from twittercomments.handlers.powhandler import PowHandler
from twittercomments.application import app
from twittercomments.as_dash import dispatcher
from twittercomments.models.tinydb.tweet import Tweet

#
# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 
# or werkzeug like routes..
# 

@app.add_route("/", pos=1, dispatch={ "get" : "_get"})
class IndexdHandler(PowHandler):
    def _get(self, index=None):
        print(" Calling IndexHandler from handlers/shorties.py: parameter index: " + str(index))
        ##external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        #retval = dispatcher(self.request, username="fake", session_id=1234)
        #self.render("index.tmpl",  dash_block=retval)
        self.redirect("/dash")

# this will be the last route since it has the lowest pos.
@app.add_route(".*", pos=0)
class ErrorHandler(PowHandler):
    def get(self):
        return self.error( template="404.tmpl", http_code=404  )

