import json
import decimal
import datetime
from pymongo import MongoClient
import Environment as env
from ..config.database import config

## Database connection string
connect_url = config[env.MONGODB_DRIVER]['url']
client: MongoClient = MongoClient(connect_url)

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

