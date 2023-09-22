import Environment as env

config = {
    'sqlite': {
        'conn_string': env.DB_CONNECTION_STRING
    },
    'pymongo': {
        'username': env.MONGODB_USER,
        'password': env.MONGODB_PASS,
        'database': env.MONGODB_DB,
        'host': env.MONGODB_HOST,
        'url': env.MONGODB_URL
    }
}