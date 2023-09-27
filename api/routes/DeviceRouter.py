from flask import Blueprint
from api.app.Controllers.DeviceController import index, find, store, delete
from api.app.Controllers.DeviceConfigController import get_by_device_id, save_config, update_config, delete_config
from api.app.Services.DeviceService import DeviceService

device_service = DeviceService()
device_router = Blueprint(device_service.get_model_path_name(), __name__)

device_router.route('/', methods=['GET'], defaults={'service': device_service}) (index)
device_router.route('/', methods=['POST'], defaults={'service': device_service}) (store)
device_router.route('/<id>', methods=['GET'], defaults={'service': device_service}) (find)
device_router.route('/<id>', methods=['DELETE'], defaults={'service': device_service}) (delete)

device_router.route('/<device_id>/device-config', methods=['GET']) (get_by_device_id)
device_router.route('/<device_id>/device-config', methods=['POST']) (save_config)
device_router.route('/<device_id>/device-config/<config_id>', methods=['PUT']) (update_config)
device_router.route('/<device_id>/device-config/<config_id>', methods=['DELETE']) (delete_config)
