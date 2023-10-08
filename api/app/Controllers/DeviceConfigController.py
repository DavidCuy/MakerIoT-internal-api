import json
import logging
import traceback
import Environment
from typing import cast, List, Tuple, Type
from flask import request
from api.app.Data.Enum.http_status_code import HTTPStatusCode
from api.utils.queue.rabbitmq import BasicMessageSender

from ..Data.Models.mongo.DeviceConfig import DeviceConfig
from ..Services.DeviceConfigService import DeviceConfigService
from ..Exceptions.APIException import APIException
from ...utils.http_utils import build_response, get_paginate_params, get_filter_params, CustomJSONDecoder

service = DeviceConfigService()

def __publish_to_queue(queue_name: str, body: str):
    try:
        queue_publisher = BasicMessageSender(Environment.SQS_DRIVE)
        queue_publisher.declare_queue(queue_name)
        queue_publisher.send_message(
            exchange='',
            routing_key=queue_name,
            body=bytes(body, 'utf-8')
        )
        queue_publisher.close()
    except Exception as e:
        print("Can't send message to queue")
        traceback.print_exc()

def get_by_device_id(device_id: str):
    _, all_configs = cast(Tuple[Type[DeviceConfig], List[DeviceConfig]], service.filter_by_column('device_id', int(device_id)))
    device_configs = list(map(lambda d: d.to_dict(), all_configs))

    return build_response(200, device_configs, jsonEncoder=CustomJSONDecoder)


def save_config(device_id: str):
    input_params = cast(dict, request.get_json())

    try:
        input_params.update({'device_id': int(device_id)})
        body = service.insert_register(input_params)
        response = json.dumps(body.to_dict(), cls=CustomJSONDecoder)
        status_code = HTTPStatusCode.OK.value

        __publish_to_queue(Environment.RABBITMQ_DEFAULT_TOPIC, json.dumps({'action': 'INSERT'}))
    except APIException as e:
        logging.exception("APIException occurred")
        response = json.dumps(e.to_dict())
        status_code = e.status_code
    except Exception:
        logging.exception("No se pudo realizar la consulta")
        body = dict(message="No se pudo realizar la consulta")
        response = json.dumps(body)
        status_code=HTTPStatusCode.UNPROCESABLE_ENTITY.value
    
    return build_response(status_code, response, is_body_str=True)

def update_config(device_id: str, config_id: str):

    input_params = request.get_json()
    try:
        body = service.update_register(config_id, input_params)
        response = json.dumps(body.to_dict(), cls=CustomJSONDecoder)
        status_code = HTTPStatusCode.OK.value

        __publish_to_queue(Environment.RABBITMQ_DEFAULT_TOPIC, json.dumps({'action': 'UPDATE'}))
    except APIException as e:
        logging.exception("APIException occurred")
        response = json.dumps(e.to_dict())
        status_code = e.status_code
    except Exception as e:
        logging.exception("Cannot make the request")
        body = dict(message="Cannot make the request")
        response = json.dumps(body)
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    return build_response(status_code, response, is_body_str=True)

def delete_config(device_id: str, config_id: str):
    try:
        body = service.delete_register(config_id)
        status_code = HTTPStatusCode.NO_CONTENT.value

        __publish_to_queue(Environment.RABBITMQ_DEFAULT_TOPIC, json.dumps({'action': 'DELETE'}))
    except APIException as e:
        logging.exception("APIException occurred")
        body = e.to_dict()
        status_code = e.status_code
    except Exception as e:
        logging.exception("Cannot make the request")
        body = dict(message="Cannot make the request")
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    return build_response(status_code, body, jsonEncoder=CustomJSONDecoder)