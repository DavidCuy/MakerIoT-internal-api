from typing import Any, Dict, List
from datetime import datetime
from mongoengine import Document, IntField, DateTimeField, StringField

class DeviceConfig(Document):
    name = StringField(required=True, max_length=200)
    device_id = IntField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
