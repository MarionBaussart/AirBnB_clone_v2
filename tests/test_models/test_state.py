#!/usr/bin/python3
""" """
from os import getenv
from tests.test_models.test_base_model import test_basemodel
from models.state import State

storageType = getenv("HBNB_TYPE_STORAGE")


class test_state(test_basemodel):
    """ """
    @classmethod
    def setUpClass(self):
        """le setup de test_state"""
        self._path_list.append("tests/test_models/test_state.py")
        self._path_list.append("models/state.py")

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.name, None)
        else:
            self.assertEqual(type(new.name), str)
