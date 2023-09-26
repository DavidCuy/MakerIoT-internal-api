from typing import Any, Dict, List
from datetime import datetime
from mongoengine import IntField, DateTimeField, StringField, DictField

from ....Core.Data.BaseMongoModel import BaseMongoModel

class DeviceConfig(BaseMongoModel):
    name = StringField(required=True, max_length=200)
    device_id = IntField(required=True)
    input_topic = StringField(max_length=512)
    input_json = DictField()
    output_json = DictField()
    output_topic = StringField(max_length=512)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
