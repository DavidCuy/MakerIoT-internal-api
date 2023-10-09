import json
import traceback
from typing import cast
from flask import Blueprint
from flask import request
from api.utils.queue.rabbitmq import BasicMessageSender
import Environment
from api.utils.http_utils import build_response

test_router = Blueprint('test', __name__)

def test_system_message():
    body = cast(dict, request.get_json())
    try:
        queue_publisher = BasicMessageSender(Environment.SQS_DRIVE)
        queue_publisher.declare_queue(Environment.RABBITMQ_SYSTEM_QUEUE)
        queue_publisher.send_message(
            exchange='',
            routing_key=Environment.RABBITMQ_SYSTEM_QUEUE,
            body=bytes(json.dumps(body), 'utf-8')
        )
        queue_publisher.close()
    except Exception as e:
        print("Can't send message to queue")
        traceback.print_exc()
    
    return build_response(200, {"message": "OK"})

test_router.route('/system-message', methods=['POST']) (test_system_message)

