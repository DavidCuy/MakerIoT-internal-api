import os
from typing import Any
from dotenv import load_dotenv

load_dotenv('.env')
def env(env_key: str, default_value: Any) -> Any:
    """ Parsea el valor de una variable de entorno a una variable utilizable para python

    Args:
        env_key (str): Nombre de la variable de entorno de
        default_value (Any): Valor por default de la variable de entorno

    Returns:
        Any: Valor designado de la variable de entorno o en su defecto la default
    """
    if env_key in os.environ:
        if os.environ[env_key].isdecimal():
            return int(os.environ[env_key])
        elif str(os.environ[env_key]).lower() == "true" or str(os.environ[env_key]).lower() == "true":
            return str(os.environ[env_key]).lower() == "true"
        else:
            return os.environ[env_key]
    else:
        return default_value

APP_NAME    = env("APP_NAME", "Flask app")
APP_URL     = env("APP_URL", "http://localhost")
STAGE       = env("STAGE", "dev")

SQLITE_PATH             = env("SQLITE_PATH", "app.db")

DB_DRIVER               = env("DB_DRIVER", "sqlite")
DB_CONNECTION_STRING    = f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), SQLITE_PATH))}"

MONGODB_DRIVER          = env("MONGODB_DRIVER", "pymongo")
MONGODB_USER            = env("MONGODB_USER", "root")
MONGODB_PASS            = env("MONGODB_PASS", "example")
MONGODB_DB              = env("MONGODB_DB", "local")
MONGODB_HOST            = env("MONGODB_HOST", "mongo")
MONGODB_PORT            = env("MONGODB_PORT", 27017)
MONGODB_URL             = f"mongodb://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOST}:27017/{MONGODB_DB}"

SERVER_CA_CERT = "ca.crt"
SERVER_CA_KEY= "ca.key"
SERVER_CSR = "server.csr"
SERVER_PRIVATE_KEY = "server.key"
SERVER_CERT = "server.crt"

SQS_DRIVE               = env("SQS_DRIVER", "rabbitmq")

RABBITMQ_USER           = env("RABBITMQ_USER", "root")
RABBITMQ_PASS           = env("RABBITMQ_PASS", "example")
RABBITMQ_HOST           = env("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT           = env("RABBITMQ_PORT", 5672)
RABBITMQ_SSL            = env("RABBITMQT_SSL", False)
RABBITMQ_URL            = f"{'amqps' if RABBITMQ_SSL else 'amqp'}://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"

RABBITMQ_DEFAULT_TOPIC   = env('RABBITMQ_DEFAULT_TOPIC', 'default-topic')
