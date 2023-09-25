import Environment as env
from .....config.database import config
from mongoengine import *

## Database connection string
config_mongo = config[env.MONGODB_DRIVER]
connect(
    config_mongo['database'],
    host=config_mongo['host'],
    port=config_mongo['port'],
    username=config_mongo['username'],
    password=config_mongo['password'],
    authentication_source='admin'
)

