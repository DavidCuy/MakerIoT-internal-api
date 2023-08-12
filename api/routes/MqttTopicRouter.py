from flask import Blueprint
from api.app.Controllers.MqttTopicController import index, find, store, update, delete, generate_certificate
from api.app.Services.MqttTopicService import MqttTopicService

mqtt_service = MqttTopicService()
mqtt_router = Blueprint(mqtt_service.get_model_path_name(), __name__)

mqtt_router.route('/', methods=['GET'], defaults={'service': mqtt_service}) (index)
mqtt_router.route('/', methods=['POST'], defaults={'service': mqtt_service}) (store)
mqtt_router.route('/<id>', methods=['GET'], defaults={'service': mqtt_service}) (find)
mqtt_router.route('/<id>', methods=['PUT'], defaults={'service': mqtt_service}) (update)
mqtt_router.route('/<id>', methods=['DELETE'], defaults={'service': mqtt_service}) (delete)

mqtt_router.route('/certs/generate', methods=['POST'], defaults={'service': mqtt_service}) (generate_certificate)
