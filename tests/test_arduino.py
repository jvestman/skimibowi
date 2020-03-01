"""Tests for SKiDL generator functions"""

import unittest
import sys
import os
sys.path.append('.')
from controller import generate_from_settings

class TestGenerator(unittest.TestCase):
    """Tests that compare complete generated SDiDL programs to expected results"""

    def assertEqualsFile(self, file1, file2):
        """Assert equality of two supplied files"""
        with open(file1, 'r') as myfile:
            generated = myfile.read()

        with open(file2, 'r') as myfile:
            target = myfile.read()

        self.maxDiff = 10000
        self.assertEqual(generated, target)
    
    def setUp(self):
        try:
            os.mkdir("tests/tmp/")
        except:
            pass

    def test_arduino_nano(self):
        """Test Arduino Nano generation"""

        generate_from_settings("tests/tmp/arduino-nano.py", "tests/arduino-nano.yml")
        self.assertEqualsFile("tests/tmp/arduino-nano.py", "tests/arduino-nano.py")

if __name__ == '__main__':
    unittest.main()
