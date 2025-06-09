
import unittest

class TestImports(unittest.TestCase):
    def test_import(self):
        import pi_home_security.hardware.boards.pi_board    
        self.assertTrue(True)
    
    def test_import_with_from(self):
        from pi_home_security.hardware.boards.pi_board import PiBoard
        self.assertTrue(True)
        
    


def main():
    unittest.main()


if __name__ == '__main__':
    main()
