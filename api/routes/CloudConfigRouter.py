from flask import Blueprint
from api.app.Controllers.CloudConfigController import index, find, store, delete
from api.app.Services import CloudConfigService

cloudConfig_service = CloudConfigService()
cloudConfig_router = Blueprint(cloudConfig_service.get_model_path_name(), __name__)

cloudConfig_router.route('/', methods=['GET'], defaults={'service': cloudConfig_service}) (index)
cloudConfig_router.route('/', methods=['POST'], defaults={'service': cloudConfig_service}) (store)
cloudConfig_router.route('/<id>', methods=['GET'], defaults={'service': cloudConfig_service}) (find)
cloudConfig_router.route('/<id>', methods=['DELETE'], defaults={'service': cloudConfig_service}) (delete)
