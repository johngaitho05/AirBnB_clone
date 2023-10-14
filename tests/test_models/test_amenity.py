#!/usr/bin/python3
"""Tests for Amenity class"""
import json
import os
import unittest
from datetime import datetime
from unittest import TestCase
from models.amenity import Amenity
from tests import BASE_DIR


class TestAmenity(TestCase):
    """Test engine for Amenity class"""

    file_name = os.path.join(BASE_DIR, 'file.json')

    def setUp(self):
        """Initializes the test model"""
        model = Amenity()
        model.name = "Test Amenity"
        model.my_number = 89
        self.model = model

    def test_id_validity(self):
        """Tests the validity of instance id"""
        self.assertEqual(type(self.model.id), str)
        self.assertEqual(len(self.model.id), 36)

    def test_dates_types(self):
        """Are they actual dates?"""
        self.assertEqual(type(self.model.created_at), datetime)
        self.assertEqual(type(self.model.updated_at), datetime)

    def test_date_equality_during_initialization(self):
        """
        created_at and updated-at should be the same after
        initialization
        """
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_str(self):
        """Tests the verbose representation of a Amenity"""
        self.assertEqual(str(self.model),
                         f"[Amenity] ({self.model.id})"
                         f" {self.model.__dict__}")

    def test_save(self):
        """Test whether Amenity object is successfully saved when save() is
        called"""
        model = Amenity()
        model.save()
        key = "Amenity.{}".format(model.id)
        with open(self.file_name, 'r') as f:
            data = json.loads(f.read() or "{}")
            self.assertIn(key, data.keys())

    def test_date_change_on_save(self):
        """Ensure updated_at is changed to a future date on save"""
        self.assertEqual(self.model.created_at, self.model.updated_at)
        self.model.save()
        self.assertTrue(self.model.updated_at > self.model.created_at)

    def test_all_keys_present(self):
        """Ensure all expected keys are present in our custom dict"""
        expected_keys = ['name', '__class__', 'updated_at', 'created_at', 'id']
        model_dict = self.model.to_dict()
        for k in expected_keys:
            self.assertIn(k, model_dict.keys())

    def test_dict_content(self):
        """ Validates the result of to_dict"""
        vals = self.model.to_dict()
        self.assertEqual(self.model.created_at.isoformat(),
                         vals.get('created_at'))
        self.assertEqual(self.model.updated_at.isoformat(),
                         vals.get('updated_at'))
        self.assertEqual('Amenity', vals.get('__class__'))
        self.assertEqual(self.model.id, vals.get('id'))
        self.assertEqual("Test Amenity", vals.get('name'))

    def test_initialization_with_kwargs(self):
        """Ascertains that we are able to recreate
        an object given its dict representation"""
        kw = self.model.to_dict()
        model = Amenity(**kw)
        self.assertEqual(self.model.id, model.id)
        self.assertEqual(self.model.created_at, model.created_at)
        self.assertEqual(self.model.updated_at, model.updated_at)
        self.assertEqual("Test Amenity", model.name)


if __name__ == '__main__':
    unittest.main()