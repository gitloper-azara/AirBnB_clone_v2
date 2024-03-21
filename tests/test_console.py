#!/usr/bin/python3
'''unittest for the console module
'''
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestCreateMethod(unittest.TestCase):
    '''Testing various cases for the console'''

    def setUp(self):
        '''setup'''
        self.command = HBNBCommand()

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_no_classname(self, mock_stdout):
        '''Test creating an instance without passing any class name'''
        self.command.onecmd('create')
        output = mock_stdout.getvalue().strip()
        self.assertIn(
            "** class name missing **", output
            )

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_nonexistent_class(self, mock_stdout):
        '''Test creating an instance with a void class'''
        self.command.onecmd('create Void')
        output = mock_stdout.getvalue().strip()
        self.assertIn(
            "** class doesn't exist **", output
            )

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_valid_instance_valid_class(self, mock_stdout):
        '''Test creating a valid instance'''
        self.command.onecmd('create User')
        output = mock_stdout.getvalue().strip()
        self.assertNotIn("** class name missing **", output)
        self.assertNotIn("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_true_output_valid_class(self, mock_stdout):
        '''Test the trueness of the output of valid class'''
        self.command.onecmd('create User')
        output = mock_stdout.getvalue().strip()
        self.assertTrue(output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_valid_instance_parameter_one(self, mock_stdout):
        '''Test passing one parameter to console'''
        self.command.onecmd('create State name="Arizona"')
        output = mock_stdout.getvalue().strip()
        self.assertNotIn("** class name missing **", output)
        self.assertNotIn("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_true_output_valid_parameter(self, mock_stdout):
        '''Test the trueness of the output of valid class'''
        self.command.onecmd('create State name="Arizona"')
        output = mock_stdout.getvalue().strip()
        self.assertTrue(output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_instance_multiple_parameters(self, mock_stdout):
        '''Test multiple parameters'''
        self.command.onecmd(
            'create Place name="My_house" city_id="0101" user_id="0101" '
            'number_rooms=4 number_bathrooms=2 max_guest=10 '
            'price_by_night=300 latitude=37.77 longitude=-122.43'
        )
        output = mock_stdout.getvalue().strip()
        self.assertTrue(output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_spaces(self, mock_stdout):
        '''Test console with spaces in parameter value'''
        self.command.onecmd('create Place name="Your big house"')
        output = mock_stdout.getvalue().strip()
        self.assertNotIn("** class name missing **", output)
        self.assertNotIn("** class doesn't exist **", output)
        self.assertTrue(output)


if __name__ == '__main__':
    unittest.main()
