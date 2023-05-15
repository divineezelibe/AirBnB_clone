#!/usr/bin/python3
"""At this point We build unittests for models/base_model.py.
Unittest classes inherits unittest.TestCase:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""

import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Functions we wrote to test the instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_str_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = date_time
        base_modelstr = base_model.__str__()
        self.assertIn("[BaseModel] (123456)", base_modelstr)
        self.assertIn("'id': '123456'", base_modelstr)
        self.assertIn("'created_at': " + date_time_repr, base_modelstr)
        self.assertIn("'updated_at': " + date_time_repr, base_modelstr)

    def test_no_args(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        base_model = BaseModel(id="540", created_at=date_time_iso, updated_at=date_time_iso)
        self.assertEqual(base_model.id, "540")
        self.assertEqual(base_model.created_at, date_time)
        self.assertEqual(base_model.updated_at, date_time)

    def test_instantiation_with_no_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)
            
class TestBaseModel_to_dict(unittest.TestCase):
    """Functions we wrote to test to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_model = BaseModel()
        self.assertTrue(dict, type(base_model.to_dict()))

    def test_to_dict_has_correct_keys(self):
        base_model = BaseModel()
        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())

    def test_to_dict_has_added_attributes(self):
        base_model = BaseModel()
        base_model.name = "My First Model"
        base_model.my_number = 89
        self.assertIn("name", base_model.to_dict())
        self.assertIn("my_number", base_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        date_time = datetime.today()
        base_model = BaseModel()
        base_model.id = "119427"
        base_model.created_at = base_model.updated_at = date_time
        to_dict = {
            'id': '119427',
            '__class__': 'BaseModel',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat()
        }
        self.assertDictEqual(base_model.to_dict(), to_dict)

    def test_contrast_to_dict_against_dict(self):
        base_model = BaseModel()
        self.assertNotEqual(base_model.to_dict(), base_model.__dict__)

    def test_to_dict_with_arg(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.to_dict(None)
            
class TestBaseModel_save(unittest.TestCase):
    """Functions we wrote to test save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        self.assertLess(first_updated_at, base_model.updated_at)

    def test_two_saves(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        second_updated_at = base_model.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_model.save()
        self.assertLess(second_updated_at, base_model.updated_at)

    def test_save_with_arg(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.save(None)

    def test_save_updates_file(self):
        base_model = BaseModel()
        base_model.save()
        base_modelid = "BaseModel." + base_model.id
        with open("file.json", "r") as f:
            self.assertIn(base_modelid, f.read())




if __name__ == "__main__":
    unittest.main()
