from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener
import simplejson as json

from tokens import *
# These values are appropriately filled in the code


class StdOutListener( StreamListener ):

    def __init__( self ):
        self.tweetCount = 0

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):
        print("Entered on_data()")
        data = json.loads(status)
        print(40*"*")
        print(data["text"])
        try:
            print(data["entities"]["hashtags"])
        except:
            print("Key entities Missing")
        print(40*"*")
        #print(status, flush = True)

        return True

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

        #s = stream.userstream()
        #stream(follow="twittercomments")
        stream.filter(track=["python"], async_=True)
        


    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()