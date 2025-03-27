import unittest
from src.utils import num, control

class TestUtils(unittest.TestCase):
    def test_num(self):
        n = num()
        result = next(n)
        self.assertEqual(result, 0)

        
    def test_control(self):
        c = control()
        result = next(c)
        self.assertEqual(result, True) 

if __name__ == "__main__":
    unittest.main()