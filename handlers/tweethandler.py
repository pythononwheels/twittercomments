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
from collections import OrderedDict

@app.add_route('/add/tweet/<int:id>', dispatch={"post" : "add_tweet"})
@app.add_route('/messages', dispatch={"get" : "get_messages"})
@app.add_route('/hashes', dispatch={"get" : "get_hashes"})
class TweetHandler(PowHandler):
    #
    # on HTTP GET this method will be called. See dispatch parameter.
    #
    
    callbacks=set()

    #@web.asynchronous
    def get_hashes(self):
        """
            returns the top 10 hashtags data
            as an Ordereddict.
        """
        print("get top hashtags")
        #data = OrderedDict(sorted(self.application.hash_cache.items(), key=lambda kv: kv[1], reverse=True))
        self.write("true")
        self.finish()

    @web.asynchronous
    def get_messages(self):
        """
            long polling handler method registering the callbacks
        """
        print("Adding callback")
        self.__class__.callbacks.add(self._callback)
        #print(self.__class__.callbacks)


    def _callback(self, html):
        print("sending callback")
        self.success(message="new tweet", data=html, pure=True)
        self.finish()

    async def fire_callbacks(self, new_tweet):
        for c in self.__class__.callbacks:
            print("fire!")
            c(new_tweet)
        
        self.__class__.callbacks = set()

    async def add_tweet(self, id=None):
        """
            just a simple hanlder sceleton. Adapt to your needs
        """ 
        #print(self.request.body)
        try:
            #data=self.request.body
            data=json.loads(self.request.body.decode('utf-8'))
            #data2=json.loads(self.request.body)
        except: 
            print("No data body!")
        
        # already seen that tweet ?
        if id in self.application.tweet_cache:
            self.application.tweet_cache[id] =  self.application.tweet_cache[id] + 1
        else:
            self.application.tweet_cache[id] = 1
        try:
            if data["retweeted_status"]["id_str"] in self.application.tweet_cache:
                self.application.tweet_cache[data["retweeted_status"]["id_str"]] += 1
                print("retweet found")
        except:
            pass
        t=Tweet()
        t.tweet_id = id
        t.text=data["text"]
        print("   #TAGS: {}".format(str(data["entities"]["hashtags"])))
        try:
            t.hashtags=data["entities"]["hashtags"]
            for htag in t.hashtags:
                if htag["text"] in self.application.hash_cache:
                    self.application.hash_cache[htag["text"]] += 1
                else:
                    self.application.hash_cache[htag["text"]] = 1
        except:
            t.hashtags=[]
        tweets_descending = OrderedDict(sorted(self.application.tweet_cache.items(), key=lambda kv: kv[1], reverse=True))
        hash_descending = OrderedDict(sorted(self.application.hash_cache.items(), key=lambda kv: kv[1], reverse=True))
        for counter, elem in enumerate(hash_descending):
            if counter < 9:
                print("hash top #{} : {} : {}".format(counter,  elem, str(hash_descending[elem])))
            else:
                break
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
        #print(r.json())
        #t.upsert()
        #print(self.__class__.callbacks)
        await self.fire_callbacks(r.json())
        #self.success(message="Added tweet id: {} ".format(str(id)), data=t.to_json(), format="json", pure=True)
        
    
