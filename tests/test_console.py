#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from tests.test_requirements import TestRequirements


class test_console(TestRequirements, unittest.TestCase):
    """ Class to test the console method """
    @classmethod
    def setUpClass(self):
        """le setup de console"""
        # self._path_list.append("tests/test_city.py")
        self._path_list.append("console.py")
