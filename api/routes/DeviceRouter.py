from flask import Blueprint
from api.app.Controllers.DeviceController import index, find, store
from api.app.Services.DeviceService import DeviceService

device_service = DeviceService()
device_router = Blueprint(device_service.get_model_path_name(), __name__)

device_router.route('/', methods=['GET'], defaults={'service': device_service}) (index)
device_router.route('/', methods=['POST'], defaults={'service': device_service}) (store)
device_router.route('/<id>', methods=['GET'], defaults={'service': device_service}) (find)

