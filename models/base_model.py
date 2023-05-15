#!/usr/bin/python3
"""this script contains the the base_model class for objects"""


import uuid
import datetime
from . import storage


class BaseModel:
    """defines all common attributes/methods for other classes: """
    def __init__(self, *args, **kwargs):
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
# =======
#                     if key == "created_at" or key == "updated_at":
#                         # Parse the string into a datetime object
#                         datetime_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
#                         value = datetime.datetime.isoformat(datetime_obj)
#                         #Trying to make value a datetime object
#                         setattr(self, key, datetime_obj)
#                     else:
#                         setattr(self, key, value)
# >>>>>>> main
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            storage.new(self)

    def __str__(self):
        class_n = self.__class__.__name__

        return "{} {} {}".format(class_n, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
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
