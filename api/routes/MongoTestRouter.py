from flask import Blueprint, request
from api.app.Data.Models.mongo.DeviceConfig import DeviceConfig
from mongoengine.queryset.queryset import QuerySet
from typing import cast
import json
from api.utils.http_utils import build_response, CustomJSONDecoder

mongo_test_router = Blueprint('mongo-test', __name__)


def query_test():
    _, device_all = DeviceConfig.all()
    devices = list(map(lambda d: d.to_dict(),device_all))
    return build_response(200, devices, jsonEncoder=CustomJSONDecoder)

def store_test():
    input_params = request.get_json()
    device = DeviceConfig(name=input_params['name'], device_id=int(input_params['device_id']))
    device.save_document()
    return build_response(200, device.to_dict(), jsonEncoder=CustomJSONDecoder)

mongo_test_router.route('/', methods=['GET']) (query_test)
mongo_test_router.route('/', methods=['POST']) (store_test)
