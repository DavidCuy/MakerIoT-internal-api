from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from ...Core.Data.BaseModel import BaseModel

class DeviceType(BaseModel):
    """ Table DeviceTypes Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        DeviceType: Instance of model
    """
    __tablename__ = 'DeviceTypes'
    id = Column("IdDeviceType", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    
    devices = relationship("Device", back_populates="deviceType")
    
    filter_columns = []
    relationship_names = ["devices"]
    search_columns = ["name"]
    
    model_path_name = "device-type"
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "name"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "name": ["required", "string"]
        }
