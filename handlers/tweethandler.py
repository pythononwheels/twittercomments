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
from twittercomments.server import hash_cache, country_cache, user_cache, tweet_cache, ofile
#import reverse_geocode
import dateutil.parser
import datetime
import pandas as pd

@app.add_route('/add/tweet/<int:tid>', dispatch={"post" : "add_tweet"})
@app.add_route('/tweetfeeder', dispatch={"post" : "tweet_feeder"})
@app.add_route('/messages', dispatch={"get" : "get_messages"})
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
        print("Adding callback...")
        self.__class__.callbacks.add(self._callback)
        #print(self.__class__.callbacks)


    def _callback(self, tweet_json):
        print("sending callback...")
        self.success(message="new tweet", data=tweet_json, pure=True)
        self.finish()

    async def fire_callbacks(self, tweet_json):
        print("fire all callbacks!")
        print(50*"-")
        tweet_json["num_tweets"] = len(tweet_cache)
        for c in self.__class__.callbacks:
            c(tweet_json)
        
        self.__class__.callbacks = set()
    
    def fill_tweet(self, t, data):
        """
            sets the tweet attributes from the given data
            maybe tweet direct
            retweet data (data["retweet_status"])
        """
        t.text=data["text"]
        #
        # update the hashtags cache
        #
        try:
            t.hashtags=data["entities"]["hashtags"]    
            for htag in t.hashtags:
                #print("adding to hashtags: {} to cache:".format(htag["text"], ))
                if htag["text"] in hash_cache:
                    hash_cache[htag["text"]] += 1
                else:
                    hash_cache[htag["text"]] = 1
        except:
            t.hashtags=[]
        #
        # update the country cache
        #
        try:
            # see: https://bitbucket.org/richardpenman/reverse_geocode/src/default/
            #country = reverse_geocode.search(data["coordinates"]["coordinates"][0])["country"]
            country = data["place"]["country_code"]
            if country in country_cache:
                country_cache[country] += 1
            else:
                country_cache[country] = 1
        except:
            print("  .... Could not identify county by coordinates")
        
        #
        # update the user cache
        #
        try:
            user_id = "@" + data["user"]["screen_name"]
            if user_id in user_cache:
                user_cache[user_id] += 1
            else:
                user_cache[user_id] = 1
        except:
            print(" ERR No User: should never happen")
        #
        # update the tweets per minute cache
        # 

        #tweets_descending = OrderedDict(sorted(self.application.tweet_cache.items(), key=lambda kv: kv[1], reverse=True))
        #hash_descending = OrderedDict(sorted(hash_cache.items(), key=lambda kv: kv[1], reverse=True))
        #for counter, elem in enumerate(hash_descending):
        #    if counter < 9:
        #        print("hash top #{} : {} : {}".format(counter,  elem, str(hash_descending[elem])))
        #    else:
        #        break
        try:
            t.user_screenname=data["user"]["screen_name"]
        except:
            t.user_screenname=""
        try:
            t.profile_image_url_https = data["user"]["profile_image_url_https"]
        except:
            t.profile_image_url_https = ""
        #
        # update the tweets cache
        #
        try:
            t.timestamp = dateutil.parser.parse(data["created_at"])
        except:
            t.timestamp = datetime.datetime.utcnow()
        return t

    async def add_tweet(self, tid=None):
        """
            just a simple hanlder sceleton. Adapt to your needs
        """ 
        try:
            data=json.loads(self.request.body.decode('utf-8'))
        except: 
            print("No data body!")

        #print("Coordinates: {}".format(data["coordinates"]))
        if "place" in data:
            print("Place: {}".format(data["place"]))

        #print("User location: {}".format(data["user"]["location"]))
        #print("User lang: {}".format(data["user"]["lang"]))
        t=Tweet()
        t.tweet_id = tid
        t = self.fill_tweet(t, data)
        tweet_cache.append(t.to_dict())
        if "retweeted_status" in data:
            t.retweeted_status=data["retweeted_status"]
        # 
        # save the tweet
        #
        t.upsert()
        #
        # now handle the retweet
        #
        if "retweeted_status" in data:
            # this is a retweet so
            # do it once more for the original tweet
            tr=Tweet()
            tr.tweet_id = data["retweeted_status"]["id_str"]
            tr = self.fill_tweet(tr, data["retweeted_status"])
            tweet_cache.append(tr.to_dict())
            #tr.upsert()
            #r=requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/"+ t.tweet_id )
            #await self.fire_callbacks(r.json())
        #print(t.to_json(),file=ofile)
        #
        # get the embed html from twitter oembed API
        #
        r=requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/"+ t.tweet_id )
        #print(r.json())
        
        #print(self.__class__.callbacks)
        await self.fire_callbacks(r.json())
        #self.success(message="Added tweet id: {} ".format(str(id)), data=t.to_json(), format="json", pure=True)
    
    async def tweet_feeder(self):
        """
            just a simple hanlder sceleton. Adapt to your needs
        """ 
        try:
            data=json.loads(self.request.body.decode('utf-8'))
        except: 
            print("No data body!")

        t=Tweet()
        t.tweet_id = data["tweet_id"]
        t.text=data["text"]
        #
        # update the hashtags cache
        #
        try:
            t.hashtags=data["hashtags"]    
            for htag in t.hashtags:
                #print("adding to hashtags: {} to cache:".format(htag["text"], ))
                if htag["text"] in hash_cache:
                    hash_cache[htag["text"]] += 1
                else:
                    hash_cache[htag["text"]] = 1
        except:
            t.hashtags=[]
        
        #
        # update the user cache
        #
        try:
            user_id = "@" + data["user_screenname"]
            if user_id in user_cache:
                user_cache[user_id] += 1
            else:
                user_cache[user_id] = 1
        except:
            print(" ERR No User: should never happen")

        try:
            t.user_screenname=data["user_screenname"]
        except:
            t.user_screenname=""
        try:
            t.profile_image_url_https = data["profile_image_url_https"]
        except:
            t.profile_image_url_https = ""
        #
        # update the tweets cache
        #
        try:
            t.timestamp = data["timestamp"]
        except:
            t.timestamp = datetime.datetime.utcnow()
        tweet_cache.append(t.to_dict())
        
        #
        # get the embed html from twitter oembed API
        #
        r=requests.get("https://publish.twitter.com/oembed?url=https://twitter.com/Interior/status/"+ t.tweet_id )
        #print(r.json())
        
        #print(self.__class__.callbacks)
        await self.fire_callbacks(r.json())
        #self.success(message="Added tweet id: {} ".format(str(id)), data=t.to_json(), format="json", pure=True)
        
    
