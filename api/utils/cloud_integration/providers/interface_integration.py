from abc import ABC, abstractmethod
from typing import Dict, List, Any

class CloudIntegrationInterface(ABC):
    MAKER = 'maker-iot'

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def rules_for_store(self, *args, **kwargs) -> Dict[str, List[Any]]:
        pass

    @abstractmethod
    def save_config(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def delete_config(self, *args, **kwargs):
        pass