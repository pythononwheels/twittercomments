#
# TinyDB Model:  Session
#
from twittercomments.models.tinydb.tinymodel import TinyModel

class Session(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        "token_expires" :   { "type": "string" },
        "refresh_token" :   { "type" : "string" }
    }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
