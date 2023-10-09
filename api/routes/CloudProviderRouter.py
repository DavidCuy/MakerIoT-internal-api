from flask import Blueprint
from api.app.Controllers.CloudProviderController import index, find
from api.app.Services.CloudProviderService import CloudProviderService

cloudProvider_service = CloudProviderService()
cloudProvider_router = Blueprint(cloudProvider_service.get_model_path_name(), __name__)

cloudProvider_router.route('/', methods=['GET'], defaults={'service': cloudProvider_service}) (index)
cloudProvider_router.route('/<id>', methods=['GET'], defaults={'service': cloudProvider_service}) (find)

