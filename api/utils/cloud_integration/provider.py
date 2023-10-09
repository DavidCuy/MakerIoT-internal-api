from .providers import CloudIntegrationInterface, AWSIntegration
from .enum_provider import CloudIntegrationEnum

CLOUD_LIST = [CloudIntegrationEnum.AWS.value]
__all__ = [CloudIntegrationEnum.ALL.value]

class CloudIntegrationNotFound(Exception):
    def __init__(self, cloud_provider) -> None:
        self.message = f'Cloud {cloud_provider} provider not found'
        super().__init__(self.message)

class CloudIntegration:
    def __init__(self, cloud_provider: str) -> None:
        if cloud_provider not in CLOUD_LIST:
            raise CloudIntegrationNotFound(cloud_provider)
        self.cloud_provider = cloud_provider
    
    def initialize(self) -> CloudIntegrationInterface:
        if self.cloud_provider.lower() == CloudIntegrationEnum.AWS.value:
            self.instance = AWSIntegration()
        else:
            raise CloudIntegrationNotFound(self.cloud_provider)
        
        return self.instance