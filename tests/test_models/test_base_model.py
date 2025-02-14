#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os
from tests.test_requirements import TestRequirements

storageType = os.getenv("HBNB_TYPE_STORAGE")


class test_basemodel(TestRequirements, unittest.TestCase):
    """ """
    @classmethod
    def setUpClass(self):
        """le setup de test_basemodel"""
        self._path_list.append("tests/test_models/test_base_model.py")
        self._path_list.append("models/base_model.py")

    def __init__(self, *args, **kwargs):
        """ __init__ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ setUp """
        pass

    def tearDown(self):
        """ tearDown """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """ test_default """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ test_kwargs """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ test_kwargs_int """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(storageType == "db", "not for here")
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ test_str """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ test_todict """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ test_kwargs_none """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """ test_id """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ test_created_at """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ test_updated_at """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
