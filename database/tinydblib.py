#
# base connection for TinyDB 
#
from twittercomments.config import database
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from twittercomments.models.tinydb.serializer import DateTimeSerializer
from tinydb.storages import MemoryStorage

tinydb = database.get("tinydb", None)

serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

if tinydb:
    conn_str = tinydb["dbname"]
    print(" ... setting it up for tinyDB: " + conn_str)
    tinydb = TinyDB(conn_str, storage=serialization)
else:
    raise Exception("I had a problem setting up tinyDB")
    

    
