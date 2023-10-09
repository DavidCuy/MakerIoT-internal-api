from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm.session import Session
from api.app.Core.Data.BaseModel import BaseModel
from api.utils.cloud_integration.provider import CloudIntegration

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
    profile = Column("profile", String, nullable=True)
    enabled = Column("enabled", Boolean, default=True)
    
    cloudProvider = relationship("CloudProvider", back_populates="cloudConfigs")
    
    filter_columns = ["id_cloud_provider", "enabled"]
    relationship_names = ["cloudProvider"]
    search_columns = ["profile"]
    
    model_path_name = "cloud-config"
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "id_cloud_provider", "profile", "enabled"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "id_cloud_provider": ["required"],
        }
    
    def after_save(self, sesion: Session, *args, **kwargs):
        self.profile = CloudIntegration(self.cloudProvider.key).initialize().save_config(**kwargs)
        try:
            sesion.commit()
        except Exception as e:
            sesion.rollback()
            raise e
    
    def before_delete(self, sesion: Session, *args, **kwargs):
        CloudIntegration(self.cloudProvider.key).initialize().delete_config(profile=self.profile)
