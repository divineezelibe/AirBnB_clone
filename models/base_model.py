#!/usr/bin/python3
"""this script contains the the base_model class for objects"""


import uuid
import datetime
from . import storage


class BaseModel:
    """defines all common attributes/methods for other classes: """
    def __init__(self, *args, **kwargs):
        """ this initializes our the instance of the class"""
        self.updated_at = datetime.datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.datetime.fromisoformat(value)
                    setattr(self, key, value)
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            storage.new(self)

    def __str__(self):
        """print a string representation of the current instance"""
        class_n = self.__class__.__name__

        return "{} {} {}".format(class_n, self.id, self.__dict__)

    def save(self):
        """this function save our object in json form inside of a file"""
        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
        """
        convert our class object to a dictionary so it can
        be saved as json
        """
        instance_dictionary = {}
        for key, value in self.__dict__.items():
            instance_dictionary[key] = value
        instance_dictionary['__class__'] = self.__class__.__name__
        instance_dictionary['created_at'] = self.created_at.isoformat()
        instance_dictionary['updated_at'] = self.updated_at.isoformat()
        for key, value in instance_dictionary.items():
            if isinstance(value, (str, int, float, bool)):
                instance_dictionary[key] = value
        return instance_dictionary
