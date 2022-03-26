import unittest
from stack import Stack

class TestPersistent(unittest.TestCase):
    def setUp(self):
        self.s = Stack()

    def test_push1(self):
        self.s.push([], 5)
        self.assertEqual(self.s.version, [[5]])

    def test_push2(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5,6], 7)
        self.assertEqual(self.s.version[0], [5])
        self.assertEqual(self.s.version[1], [5, 6])
        self.assertEqual(self.s.version[2], [5, 6, 7])

    def test_push3(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.s.push([5], 8)
        self.assertEqual(self.s.version[0], [5])
        self.assertEqual(self.s.version[1], [5, 6])
        self.assertEqual(self.s.version[2], [5, 6, 7])
        self.assertEqual(self.s.version[3], [5, 8])

    def test_pop_and_save_new_version(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.s.pop([5, 6, 7])
        self.assertEqual(self.s.version[3], [5, 6])

    def test_pop_and_save_new_version2(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.s.pop([5, 6, 7])
        self.s.pop([5, 6])
        self.assertEqual(self.s.version[3], [5, 6])
        self.assertEqual(self.s.version[4], [5])