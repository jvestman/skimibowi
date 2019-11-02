"""Tests for SKiDL generator functions"""

import unittest
import sys
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

    def test_empty_board(self):
        """Test empty board"""

        generate_from_settings("tests/tmp/empty.py", "tests/empty.yml")
        self.assertEqualsFile("tests/tmp/empty.py", "tests/empty.py")

    def test_basic_esp12(self):
        """Test basic ESP12 breakout with FTDI -header"""

        generate_from_settings("tests/tmp/basic-esp12.py", "tests/basic-esp12.yml")
        self.assertEqualsFile("tests/tmp/basic-esp12.py", "tests/basic-esp12.py")

    def test_esp12_reset_and_flash(self):
        """Test generation of ESP12 breakout with reset line, reset button and flash button"""

        generate_from_settings("tests/tmp/esp12-reset-flash.py", "tests/esp12-reset-flash.yml")
        self.assertEqualsFile("tests/tmp/esp12-reset-flash.py", "tests/esp12-reset-flash.py")

    def test_esp12_ftdi_header(self):
        """Test ESP FTDI header generation"""

        generate_from_settings("tests/tmp/esp12-ftdi-header.py", "tests/esp12-ftdi-header.yml")
        self.assertEqualsFile("tests/tmp/esp12-ftdi-header.py", "tests/esp12-ftdi-header.py")


if __name__ == '__main__':
    unittest.main()
