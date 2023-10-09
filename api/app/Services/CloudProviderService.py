from api.app.Core.Services.BaseService import BaseService
from api.app.Data.Models import CloudProvider


class CloudProviderService(BaseService):
    def __init__(self) -> None:
        super().__init__(CloudProvider)
