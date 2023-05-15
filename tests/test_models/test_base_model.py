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
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_no_args(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_time = datetime.today()
        dt_iso = date_time.isoformat()
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
        base_model.created_at = bm.updated_at = dt
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
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
