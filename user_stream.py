from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener
import simplejson as json

from tokens import *
# These values are appropriately filled in the code
import urllib
from tornado.httpclient import HTTPClient
import requests
import sys


class StdOutListener( StreamListener ):

    def __init__( self ):
        self.tweetCount = 0

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):
        #print("Entered on_data()")
        data = json.loads(status)
        print(40*"*")
        print(data["text"])
        try:
            print(data["entities"]["hashtags"])
        except:
            print("Key entities Missing")
        headers = {'content-type': 'application/json'}

        print(40*"*")
        r = requests.post("http://localhost:8080/add/tweet/"+str(data["id_str"]), data=json.dumps(data), headers=headers)
        #print(status, flush = True)
        print(40*"-")
        
        print("Response: " + str(r))
        print(40*"-")
        return True
    
    def handle_request_response(self, response):
        print(str(response))

    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status, flush = True)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_error( self, status ):
        print(status)

def main():

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)

        api = API(auth)

        # If the authentication was successful, you should
        # see the name of the account print out
        print(api.me().name)

        stream = Stream(auth=api.auth, listener=StdOutListener())
        try:
            keywords = str.split(sys.argv[1], " ")
        except:
            keywords=["python", "Python", "python3"]
        
        print("Looking for: {}".format(keyword))
        #s = stream.userstream()
        #stream(follow="twittercomments")
        stream.filter(track=[keyword], async_=True)
        


    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()