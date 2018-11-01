#from twittercomments.handlers.base import BaseHandler
from twittercomments.handlers.powhandler import PowHandler
from twittercomments.config import myapp
from twittercomments.application import app
import simplejson as json
import tornado.web
from tornado import gen
# Please import your model here. (from yourapp.models.dbtype)
from twittercomments.models.tinydb.session import Session
from twittercomments.as_dash import dispatcher
from twittercomments.models.tinydb.tweet import Tweet

@app.add_route("/dash.*", dispatch={"get" :"dash"})
@app.add_route("/_dash.*", dispatch={"get" :"dash_ajax", "post": "dash_ajax"})
#@app.add_route('/dash/test/<int:testval>', dispatch={"get" : "_get_method"})
class Dash(PowHandler):
    #
    # Sample dash handler to embedd dash into own website.
    #  
    def dash(self, **kwargs):
        """ """
        print("processing dash method")
        
        #session_id=self.get_secure_cookie("tcsession")
        #if not session_id:
        #    self.redirect("/login")
        #s=Session()
        #print("session ID from cookie: " + str(session_id))
        #current_session=s.find_one(s.Query.id==session_id.decode("utf-8"))
        #if not current_session:
        #    self.redirect("/login")
        #print(" working with Session: {}".format(current_session.id))
        
        # 
        # This is the place where dash is called.
        # dispatcher returns the HMTL including title, css, scripts and config via => dash.Dash.index()
        # (See: in as_dash.py => myDash.index)
        # You can then insert the returned HTML into your template.
        # I do this below in the self.success call => see base_dash.bs4 template (mustache like syntax)
        #
        #external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        retval = dispatcher(self.request, username="fake", session_id=1234)
        #print("dash dispatcher got cut to [0:200]" + str(retval)[0:200])
        
        #
        # get all tweets to get some data
        #
        m=Tweet()
        res=m.get_all()
        try:
            num_tweets=len(list(res))
        except:
            num_tweets=None
        # 
        # this is the render template call which embeds the dash code (dash_block=retval)
        # from dispatcher (see above)
        #self.success(template="index.tmpl", dash_block=retval, data=res, num_tweets=num_tweets )
        #self.render("base_dash.tmpl", dash_block=retval)
        self.render("index2.tmpl", dash_block=retval)

    
    def dash_ajax(self):
        """ 
            respond to the dash ajax / react request's 
        """
        #
        # get some session info
        #
        name="NONE"
        print(" processing dash_ajax method")
        #session_id=self.get_secure_cookie("tcsession")
        #if not session_id:
        #    self.redirect("/login")
        #s=Session()
        #print("session ID from cookie: " + str(session_id))
        #current_session=s.find_one(s.Query.id==session_id.decode("utf-8"))
        #if not current_session:
        #    self.redirect("/login")
        #print(" working with Session: {}".format(current_session.id))

        #name=current_session.user_email.split("@")[0]
        #
        # now hand over to the dispatcher
        #
        retval = dispatcher(self.request, username="fake", session_id=1234, tcapp=self.application)
        #print("dash_ajax I got retval: {}".format(str(retval)[0:200]))
        #print("dash_ajax I got username(from session): {}".format(name))
        # finish
        self.set_header('Content-Type', 'application/json')
        self.write(retval)