from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from ...Core.Data.BaseModel import BaseModel

class CloudConfig(BaseModel):
    """ Table CloudConfigs Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        CloudConfigType: Instance of model
    """
    __tablename__ = 'CloudConfigs'
    id = Column("IdCloudConfig", Integer, primary_key=True)
    id_cloud_provider = Column("IdCloudProvider", Integer, ForeignKey("CloudProviders.IdCloudProvider"), nullable=False)
    profile = Column("profile", String, nullable=False)
    enabled = Column("enabled", Boolean, default=False)
    
    cloudProvider = relationship("CloudProvider", back_populates="cloudConfigs")
    
    filter_columns = ["id_cloud_provider", "enabled"]
    relationship_names = ["cloudProvider"]
    search_columns = ["profile"]
    
    model_path_name = "cloud-config"
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "id_cloud_provider", "profile"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "id_cloud_provider": ["required"],
            "profile": ["required", "string"]
        }
