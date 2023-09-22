from __future__ import annotations
import json
from json.encoder import JSONEncoder
from typing import Any, Dict, List, Type, cast
from operator import and_, or_
from sqlalchemy import Column, Integer, orm
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from typing import List
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from ....database.DBMongoConnectionModel import client, MongoEncoder

class BaseMongoModel(Collection):
    """ Base model for a child classes implementations

    Args:
        Base (Any): SQLAlchemy declarative base

    Raises:
        e: Exceptions for not implemented functions

    Returns:
        BaseModel: Instace of BaseModel class
    """

    ## Indicate it is an abstract class (not 100% completed y going to be done in child classes)
    __abstract__ = True
    ## Model identifier. All tables from database should have
    id: ObjectId
    db_name: str = "local"
    collection_name: str = ""
    model_path_name = ""
    
    filter_columns = []

    @property
    def attrs(self) -> List[str]:
        """ Returns a list of the attributes of an object

        Returns:
            List[str]: Attributes
        """
        preliminar = list(filter(lambda prop: not str(prop).startswith('_'), type(self).__dict__.keys()))
        display_member = self.display_members()
        return list(set(preliminar) & set(display_member)) if len(display_member) > 0 else display_member

    def all(self):
        """ Get all documents from a collection

        Args:
            self (self): Instance of of class

        Returns:
            List[Type[Any]]: List of elements mapped from database table
        """
        cursor = client[self.db_name][self.collection_name]
        return cursor, [element for element in cursor.find({})]
    
    def get_paginated(self, page: int = 1, per_page: int = 10):
        page = page - 1
        cursor = client[self.db_name][self.collection_name]
        return cursor.find({}).limit(per_page).skip(page*per_page)
    
    def find(self, id: str):
        """ Search a document by id

        Args:
            self (class): Instance class method
            id (str): Document identifier

        Returns:
            Type[Any]: The document that have a coincidence with the identifier
        """
        if id != '':
            cursor = client[self.db_name][self.collection_name]
            return cursor.find_one({"_id": ObjectId(id)})
    
    def filter_by(self, column_name: str, value, paginated: bool = False, page: int = 1, per_page: int = 10, first = False):
        """ Gets all documents that match with the specified filter

        Args:
            self (class): Instance class method
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            List[Type[Any]]: List of documents that match with filter
        """
        filter_dict = {
            column_name: value
        }
        return self.filters(filter_dict, paginated, page, per_page, first)
    
    def get_one(self, column_name: str, value):
        """ Gets the first row that matches the filter

        Args:
            self (class): Instance class method
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            Type[Any]: First register that match with filter
        """
        filter_dict = {
            column_name: value
        }
        return client[self.db_name][self.collection_name].find_one(filter_dict)
    
    def filters(self, filters: dict, paginated: bool = False, page: int = 1, per_page: int = 10, first: bool = False):
        cursor = client[self.db_name][self.collection_name]

        if first:
            return cursor, cursor.find_one(filters)

        if paginated:
            page = page - 1
            return cursor, cursor.find(filters).limit(per_page).skip(page*per_page)
        return cursor, cursor.find({})

    def before_save(self, *args, **kwargs):
        """ Method to execute before save a row in database (polimorfism)
        """
        pass

    def after_save(self, *args, **kwargs):
        """ Method to execute after save a row in database (polimorfismo)
        """
        pass
    
    def save(self, *args, **kwargs):
        """ Save a register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.

        Raises:
            e: In case of error, the register will be erased and raise an Exception
        """
        self.before_save(*args, **kwargs)
        cursor = client[self.db_name][self.collection_name]
        cursor.insert_one(self.to_dict())

        self.after_save(*args, **kwargs)
        return self

    def before_update(self, *args, **kwargs):
        """ Method to execute before update a row in database (polimorfism)
        """
        pass

    def after_update(self, *args, **kwargs):
        """ Method to execute after update a row in database (polimorfism)
        """
        pass

    def update(self, object: dict, *args, **kwargs):
        """ Update a specified register in database

        Args:
            session (Session): Database session
            object (dict): Dictionary with only the field to update
        """
        self.before_update(*args, **kwargs, **object)
        keys = self.get_keys()
        for key in keys:
            if key in object:
                self.__setattr__(key, object[key])
        
        filter_update = {"_id": self.id}
        newvalues = { "$set": self.to_dict() }
        
        cursor = client[self.db_name][self.collection_name]
        cursor.update_one(filter_update, newvalues)

        self.after_update(*args, **kwargs)
        return self
    
    def before_delete(self, *args, **kwargs):
        """ Method to execute before update a row in database (polimorfism)
        """
        pass

    def after_delete(self, *args, **kwargs):
        """ Method to execute after update a row in database (polimorfism)
        """
        pass

    def delete(self, commit=True, *args, **kwargs):
        """ Delete a specified register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.
        """
        self.before_delete(*args, **kwargs)
        cursor = client[self.db_name][self.collection_name]
        filter_delete = {"_id": self.id}
        cursor.delete_one(filter_delete)
        self.after_delete(*args, **kwargs)
    
    
    @classmethod
    def get_keys(cls_) -> List[str]:
        """ Get all attributes of class

        Args:
            cls_ (Type[BaseModel]): Child class method

        Returns:
            List[str]:  Attributes
        """
        return list(filter(lambda prop: not str(prop).startswith('_'), cls_.__dict__.keys()))

    
    def to_dict(self, jsonEncoder: JSONEncoder = MongoEncoder, circular: bool = True, encoder_extras: dict = {}) -> dict:
        return json.loads(json.dumps(self, cls=jsonEncoder, check_circular=circular, **encoder_extras))


    def __repr__(self) -> str:
        """ Model representation

        Returns:
            str: Model output string formatted
        """
        attr_array = [f"{attr}={self.__getattribute__(attr)}" for attr in self.attrs]
        args_format = ",".join(attr_array)
        return f"<{type(self).__name__}({args_format})>"


