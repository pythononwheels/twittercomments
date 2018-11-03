import simplejson as json
import urllib
from tornado.httpclient import HTTPClient
import requests
import sys
from twittercomments.models.tinydb.tweet import Tweet
import random
import time
#
# This program will feed the server with a random
# number of tweets from the db
#

def main():
    t=Tweet()
    headers = {'content-type': 'application/json'}
    while True:
        # get all tweets
        reslist=list(t.get_all())
        num_tweets=len(reslist)
        # pick one (randomly)
        num=random.randint(0,num_tweets-1)
        # send the tweet to the server
        print(60*"-")
        print(reslist[num])
        r = requests.post("http://localhost:8080/tweetfeeder", data=reslist[num].to_json(), headers=headers)
        print("Response: " + str(r))
        print(60*"-")
        wait=random.randint(0,5)
        time.sleep(wait)

if __name__ == '__main__':
    main()