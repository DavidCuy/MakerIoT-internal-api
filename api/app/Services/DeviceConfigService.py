from api.app.Core.Services.BaseMongoService import BaseMongoService
from api.app.Data.Models.mongo import DeviceConfig


class DeviceConfigService(BaseMongoService):
    def __init__(self) -> None:
        super().__init__(DeviceConfig)
