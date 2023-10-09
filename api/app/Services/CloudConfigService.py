from api.app.Core.Services.BaseService import BaseService
from api.app.Data.Models import CloudConfig
from api.utils.cloud_integration.provider import CloudIntegration


class CloudConfigService(BaseService):
    def __init__(self) -> None:
        super().__init__(CloudConfig)
    
    def update_rules_store_from_provider(self, provider: str):
        return CloudIntegration(provider).initialize().rules_for_store()
