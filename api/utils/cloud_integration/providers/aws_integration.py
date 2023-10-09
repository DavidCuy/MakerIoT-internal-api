import json
from .interface_integration import CloudIntegrationInterface
from api.utils.storage import Storage

class AWSIntegration(CloudIntegrationInterface):
    def save_config(self, account_id: str, access_key_id: str, access_key_secret: str, region: str = 'us-east-1') -> str:
        profile = f'{self.MAKER}_{account_id}'
        config = {
            'aws_access_key_id': access_key_id,
            'aws_secret_access_key': access_key_secret,
            'region_name': region
        }
        Storage('local').put(f'{profile}.json', bytes(json.dumps(config, indent=2), 'utf-8'))
        return profile
    
    def rules_for_store(self):
        return {
            "account_id": ["required"],
            "access_key_id": ["required", "string"],
            "access_key_secret": ["required", "string"]
        }
    
    def delete_config(self, profile: str):
        Storage('local').delete(f'{profile}.json')