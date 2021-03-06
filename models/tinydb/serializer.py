from tinydb_serialization import Serializer
from datetime import datetime
from twittercomments.config import myapp
# see: https://github.com/msiemens/tinydb/issues/48
# and: https://github.com/msiemens/tinydb-serialization

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        #return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return obj.strftime(myapp["date_format"])
    def decode(self, s):
        #return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
        return datetime.strptime(s, myapp["date_format"])