#
# TinyDB Model:  Tweet
#
from twittercomments.models.tinydb.tinymodel import TinyModel

class Tweet(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'text'                      :   { 'type' : 'string', 'maxlength' : 300 },
        'tweet_id'                  :   { 'type' : 'string' },
        'hashtags'                  :   { 'type' : 'list', "default" : [] },
        "user_id"                   :   { "type" : "string" },
        "user_screenname"           :   { "type" : "string"},
        "profile_image_url_https"   :   { "type" : "string"}
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
