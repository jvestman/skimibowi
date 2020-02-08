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
            myfile.close()

        with open(file2, 'r') as myfile:
            target = myfile.read()

        self.maxDiff = 10000
        self.assertEqual(generated, target)

    def setUp(self):
        try:
            os.mkdir("tests/tmp/")
        except:
            pass

    def test_empty_settings(self):
        """Test empty board"""

        generate_from_settings("tests/tmp/zero.py", "tests/zero.yml")
        self.assertEqualsFile("tests/tmp/zero.py", "tests/zero.py")

    def test_empty_board(self):
        """Test empty board"""

        generate_from_settings("tests/tmp/empty.py", "tests/empty.yml")
        self.assertEqualsFile("tests/tmp/empty.py", "tests/empty.py")

    def test_esp12(self):
        """Test basic ESP12"""

        generate_from_settings("tests/tmp/esp12.py", "tests/esp12.yml")
        self.assertEqualsFile("tests/tmp/esp12.py", "tests/esp12.py")

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
    
    def test_esp12_board1(self):
        """Test ESP12 board 1"""

        generate_from_settings("tests/tmp/board1.py", "tests/board1.yml")
        self.assertEqualsFile("tests/tmp/board1.py", "tests/board1.py")

    def test_wemos_d1_mini_18b20u(self):
        """Test ESP12 board 1"""

        generate_from_settings("tests/tmp/wemos_d1_mini_18b20u.py", "tests/wemos_d1_mini_18b20u.yml")
        self.assertEqualsFile("tests/tmp/wemos_d1_mini_18b20u.py", "tests/wemos_d1_mini_18b20u.py")
    

if __name__ == '__main__':
    unittest.main()
