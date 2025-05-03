
import unittest

class TestImports(unittest.TestCase):
    def test_import(self):
        import pi_home_security.components.pi_board    
        self.assertTrue(True)
    
    def test_import_with_from(self):
        from pi_home_security.components.pi_board import PiBoard
        self.assertTrue(True)
        
        