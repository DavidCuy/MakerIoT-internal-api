from flask import Blueprint, request
from api.app.Data.Models.mongo.DeviceConfig import DeviceConfig
from mongoengine.queryset.queryset import QuerySet
from typing import cast
import json
from api.utils.http_utils import build_response, CustomJSONDecoder

mongo_test_router = Blueprint('mongo-test', __name__)


def query_test():
    devices = json.loads(cast(QuerySet, DeviceConfig.objects()).to_json())
    return build_response(200, devices, jsonEncoder=CustomJSONDecoder)

def store_test():
    input_params = request.get_json()
    device = DeviceConfig(name=input_params['name'], device_id=int(input_params['device_id']))
    device.save()
    ret_data = json.loads(cast(QuerySet, device).to_json())
    return build_response(200, ret_data, jsonEncoder=CustomJSONDecoder)

mongo_test_router.route('/', methods=['GET']) (query_test)
mongo_test_router.route('/', methods=['POST']) (store_test)
