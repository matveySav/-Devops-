import unittest
from app import count_divisors

class TestApp(unittest.TestCase):
    def test_value(self):
        self.assertEqual(count_divisors(1),2)
        self.assertEqual(count_divisors(100),9)
        self.assertEqual(count_divisors(64),7)
        self.assertEqual(count_divisors(17),2)
        self.assertEqual(count_divisors(111),4)

if __name__ == '__main__':
    unittest.main(verbosity=1)
