import sys
import unittest
from copy import copy
from unittest import mock

from . import mock_builtin

sys.modules["__builtins__"] = mock_builtin

__all__ = ["ORIG_POS", "ORIG_SIZE", "BaseCase", "mock", 'mock_builtin', 'unittest']

ORIG_SIZE = copy(mock_builtin.__map_size__)
ORIG_POS = copy(mock_builtin.__pos__)

class BaseCase(unittest.TestCase):
    def _reset_pos(self):
        mock_builtin.__pos__ = copy(ORIG_POS)
    def _reset_map_size(self):
        mock_builtin.__map_size__ = copy(ORIG_SIZE)
    def _check_map_size(self, expected: int):
        self.assertEqual(mock_builtin.__map_size__, expected)
    def _check_pos(self, expected: tuple[int, int, int]):
        self.assertEqual(mock_builtin.__pos__, list(expected))
    def tearDown(self):
        mock_builtin.reset_all()
        self._reset_map_size()
        self._reset_pos()

    def _set_pos(self, pos: tuple[int, int, int]):
        mock_builtin.__pos__ = list(pos)

    def _set_map_size(self, size: int):
        mock_builtin.__map_size__ = size
