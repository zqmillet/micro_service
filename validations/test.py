import unittest

class JustForTest(unittest.TestCase):
    def runTest(self):
        length = 10
        self.assertEqual(10, length)

if __name__ == '__main__':
    unittest.main()
