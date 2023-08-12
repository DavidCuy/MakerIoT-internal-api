import os

import Environment as env

config = {
    'local': {
        'default': {
            'initial_path': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storage", "local"))
        },
        'server-credentials': {
            'initial_path': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storage", "credentials", "server"))
        },
        'client-credentials': {
            'initial_path': os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storage", "credentials", "clients"))
        }
    }
}