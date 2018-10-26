#from twittercomments.handlers.base import BaseHandler
from twittercomments.handlers.powhandler import PowHandler
from twittercomments.config import myapp
from twittercomments.application import app
import simplejson as json
from tornado import web
from tornado import gen
# Please import your model here. (from yourapp.models.dbtype)
from twittercomments.models.tinydb.tweet import Tweet
import requests

@app.add_route('/add/tweet/<int:id>', dispatch={"post" : "add_tweet"})
@app.add_route('/messages/', dispatch={"get" : "get_messages"})
class TweetHandler(PowHandler):
    #
    # on HTTP GET this method will be called. See dispatch parameter.
    #
    
    callbacks=set()

    @web.asynchronous
    def get_messages(self):
        """
            long polling handler method registering the callbacks
        """
        print("Adding callback")
        self.__class__.callbacks.add(self._callback)
        print(self.__class__.callbacks)


    def _callback(self, html):
        print("sending callback")
        self.success(message="new tweet", data=html, pure=True)
        self.finish()

    def fire_callbacks(self, new_tweet):
        for c in self.__class__.callbacks:
            print("fire!")
            c(new_tweet)
        
        self.__class__.callbacks = set()

    def add_tweet(self, id=None):
        """
            just a simple hanlder sceleton. Adapt to your needs
        """ 
        print(self.request.body)
        try:
            #data=self.request.body
            data=json.loads(self.request.body.decode('utf-8'))
            #data2=json.loads(self.request.body)
        except: 
            print("No data body!")
        t=Tweet()
        #print(type(data2))
        #print(data2["id_str"])

        #print("Incoming data body:")
        #print(str(data))
        #t.init_from_json(data)
        t.tweet_id = id
        t.text=data["text"]
        try:
            t.hashtags=data["entities"]["hastags"]
        except:
            t.hashtags=[]
        try:
            t.user_screenname=data["user"]["screen_name"]
        except:
            t.user_screenname=""
        try:
            t.profile_image_url_https = data["user"]["profile_image_url_https"]
        except:
            t.profile_image_url_https = ""
        #
        # get the embed html from twitter oembed API
        #
        r=requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/"+ t.tweet_id )
        print(r.json())
        #t.upsert()
        print(self.__class__.callbacks)
        self.fire_callbacks(r.json())
        #self.success(message="Added tweet id: {} ".format(str(id)), data=t.to_json(), format="json", pure=True)
        
    
