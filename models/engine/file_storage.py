#!/usr/bin/python3
"""
this class is a filestorage that serializes instances to a JSON fil
and deserializes JSON file to instances
"""
import json
import os


class FileStorage:
    """this is the storage for every instance of our models"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns all the object instance we have
        """
        return self.__objects

    def new(self, obj):
        """
        this function adds the new objects to __objects dictionary which
        adds files to be stored in json
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        stores our json object into file.json
        """
        data = {}
        for key, value in self.__objects.items():
            data[key] = value.to_dict()
        with open(self.__file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file)

    def reload(self):
        """convert json object back to our class object"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, mode="r", encoding="utf-8")\
                 as file:
                data = json.load(file)
                for key, obj_dict in data.items():
                    model = ""
                    class_name, obj_id = key.split(".")
                    if class_name == "BaseModel":
                        model = "base_model"
                    if class_name == "User":
                        model = "user"
                    if class_name == "State":
                        model = "state"
                    if class_name == "City":
                        model = "city"
                    if class_name == "Amenity":
                        model = "amenity"
                    if class_name == "Place":
                        model = "place"
                    if class_name == "Review":
                        model = "review"
                    module = \
                        __import__(f"models.{model}", fromlist=[class_name])
                    cls = getattr(module, class_name)
                    obj = cls(**obj_dict)
                    self.__objects[key] = obj
