from typing import Any, Dict, List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from ...Core.Data.BaseModel import BaseModel

class Device(BaseModel):
    """ Table Devices Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        DeviceType: Instance of model
    """
    __tablename__ = 'Devices'
    id = Column("IdDevice", Integer, primary_key=True)
    id_device_type = Column("IdDeviceType", Integer, ForeignKey("DeviceTypes.IdDeviceType"), nullable=False)
    name = Column("name", String, nullable=False)
    serial = Column("serial", String, nullable=False)
    
    deviceType = relationship("DeviceType", back_populates="devices")
    
    filter_columns = ["id_device_type"]
    relationship_names = ["deviceType"]
    search_columns = ["name", "serial"]
    
    model_path_name = "device"
    
    @classmethod
    def display_members(cls_) -> List[str]:
        return [
            "id", "id_device_type", "name", "serial"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "id_device_type": ["required"],
            "name": ["required", "string"],
            "serial": ["required", "string"]
        }
