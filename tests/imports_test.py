
import unittest

class TestImports(unittest.TestCase):
    def test_import(self):
        import rpi_home_security.pi_board    
        self.assertTrue(True)
    
    # def test_import_with_from(self):
    #     from rpi_home_security.pi_board import PiBoard
    #     self.assertTrue(True)
        
        