import unittest
from stack import Stack


class TestPersistent(unittest.TestCase):
    def setUp(self):
        self.s = Stack()

    def test_push_without_elements(self):
        self.s.push([], 5)
        self.assertEqual(self.s.version, [[5]])

    def test_push_three_element(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.assertEqual(self.s.version[0], [5])
        self.assertEqual(self.s.version[1], [5, 6])
        self.assertEqual(self.s.version[2], [5, 6, 7])

    def test_push_in_first_version(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.s.push([5], 8)
        self.assertEqual(self.s.version[0], [5])
        self.assertEqual(self.s.version[1], [5, 6])
        self.assertEqual(self.s.version[2], [5, 6, 7])
        self.assertEqual(self.s.version[3], [5, 8])

    def test_pop_from_last_version(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.s.pop([5, 6, 7])
        self.assertEqual(self.s.version[3], [5, 6])

    def test_pop_two_elements(self):
        self.s.push([], 5)
        self.s.push([5], 6)
        self.s.push([5, 6], 7)
        self.s.pop([5, 6, 7])
        self.s.pop([5, 6])
        self.assertEqual(self.s.version[3], [5, 6])
        self.assertEqual(self.s.version[4], [5])

    def test_pop_without_element(self):
        self.s.push([], 5)
        self.s.pop([5])
        self.s.pop([])
        self.assertEqual(self.s.version[1], [])
