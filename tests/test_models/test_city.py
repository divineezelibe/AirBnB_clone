#!/usr/bin/python3
"""This module will define unittests for models/city.py.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city_ = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city_))
        self.assertNotIn("state_id", city_.__dict__)

    def test_name_is_public_class_attribute(self):
        city_ = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city_))
        self.assertNotIn("name", city_.__dict__)

    def test_two_cities_unique_ids(self):
        city_1 = City()
        city_2 = City()
        self.assertNotEqual(city_1.id, city_2.id)

    def test_two_cities_different_created_at(self):
        city_1 = City()
        sleep(0.05)
        city_2 = City()
        self.assertLess(city_1.created_at, city_2.created_at)

    def test_two_cities_different_updated_at(self):
        city_1 = City()
        sleep(0.05)
        city_2 = City()
        self.assertLess(city_1.updated_at, city_2.updated_at)

    def test_str_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        city_ = City()
        city_.id = "123456"
        city_.created_at = city_.updated_at = date_time
        city_str = city_.__str__()
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + date_time_repr, city_str)
        self.assertIn("'updated_at': " + date_time_repr, city_str)

    def test_args_unused(self):
        city_ = City(None)
        self.assertNotIn(None, city_.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        city_ = City(id="345", created_at=date_time_iso, updated_at=date_time_iso)
        self.assertEqual(city_.id, "345")
        self.assertEqual(city_.created_at, date_time)
        self.assertEqual(city_.updated_at, date_time)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        city_ = City()
        sleep(0.05)
        first_updated_at = city_.updated_at
        city_.save()
        self.assertLess(first_updated_at, city_.updated_at)

    def test_two_saves(self):
        city_ = City()
        sleep(0.05)
        first_updated_at = city_.updated_at
        city_.save()
        second_updated_at = city_.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city_.save()
        self.assertLess(second_updated_at, city_.updated_at)

    def test_save_with_arg(self):
        city_ = City()
        with self.assertRaises(TypeError):
            city_.save(None)

    def test_save_updates_file(self):
        city_ = City()
        city_.save()
        city_id = "City." + city_.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        city_ = City()
        self.assertIn("id", city_.to_dict())
        self.assertIn("created_at", city_.to_dict())
        self.assertIn("updated_at", city_.to_dict())
        self.assertIn("__class__", city_.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city_ = City()
        city_.middle_name = "School"
        city_.my_number = 89
        self.assertEqual("School", city_.middle_name)
        self.assertIn("my_number", city_.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city_ = City()
        city__dict = city_.to_dict()
        self.assertEqual(str, type(city__dict["id"]))
        self.assertEqual(str, type(city__dict["created_at"]))
        self.assertEqual(str, type(city__dict["updated_at"]))

    def test_to_dict_output(self):
        date_time = datetime.today()
        city_ = City()
        city_.id = "123456"
        city_.created_at = city_.updated_at = date_time
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(city_.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        city_ = City()
        self.assertNotEqual(city_.to_dict(), city_.__dict__)

    def test_to_dict_with_arg(self):
        city_ = City()
        with self.assertRaises(TypeError):
            city_.to_dict(None)


if __name__ == "__main__":
    unittest.main()
