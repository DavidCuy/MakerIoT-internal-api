from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from ...Core.Data.BaseModel import BaseModel

class CloudProvider(BaseModel):
    """ Table CloudProviders Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        CloudProvider: Instance of model
    """
    __tablename__ = 'CloudProviders'
    id = Column("IdCloudProvider", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    key = Column("key", String, nullable=False)
    
    cloudConfigs = relationship("CloudConfig", back_populates="cloudProvider")
    
    filter_columns = []
    relationship_names = ["cloudConfigs"]
    search_columns = ["name", "key"]
    
    model_path_name = "cloud-provider"
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "name", "key"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "name": ["required", "string"],
            "key": ["required", "string"]
        }
