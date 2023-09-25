from typing import Any, Dict, List
from datetime import datetime
from mongoengine import IntField, DateTimeField, StringField

from ....Core.Data.BaseMongoModel import BaseMongoModel

class DeviceConfig(BaseMongoModel):
    name = StringField(required=True, max_length=200)
    device_id = IntField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
