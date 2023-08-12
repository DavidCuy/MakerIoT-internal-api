from flask import Blueprint
from api.app.Controllers.DeviceTypeController import index, find
from api.app.Services.DeviceTypeService import DeviceTypeService

deviceType_service = DeviceTypeService()
deviceType_router = Blueprint(deviceType_service.get_model_path_name(), __name__)

deviceType_router.route('/', methods=['GET'], defaults={'service': deviceType_service}) (index)
deviceType_router.route('/<id>', methods=['GET'], defaults={'service': deviceType_service}) (find)

