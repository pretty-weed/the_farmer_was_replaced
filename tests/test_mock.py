from collections import namedtuple

from .base_test import *
from .mock_builtin import East, North, South, West

SetPosCase = namedtuple("SetPosCase", ["args", "kwargs", "expected"])


_POS_CASES = [
    SetPosCase([1, 2, 3], {}, (1,2,3)),
    SetPosCase([1], {}, (1, 0, 0)),
    SetPosCase([], {'x': 4, 'y': 5, 'z': 6}, (4, 5, 6)),
    SetPosCase([2], {'z':8}, (2, 0, 8))
]

class TestGetters(BaseCase):
    def test_getters(self):
        self.assertEqual(mock_builtin.__pos__, [0, 0, 0])
        self.assertEqual(mock_builtin.__map_size__, 12)
        mock_builtin.__pos__ = [3, 4, 5]
        mock_builtin.__map_size__ = 8

        self.assertEqual(mock_builtin.get_pos(), (3, 4, 5))
        self.assertEqual((mock_builtin.get_pos_x(), mock_builtin.get_pos_y()), (3, 4))
        self.assertEqual(mock_builtin.get_world_size(), 8)

class TestSetup(BaseCase):
    def _check_pos(self, expected: tuple[int, int, int]):
        with self.subTest("Checking get_pos"):
            self.assertEqual(mock_builtin.get_pos(), tuple(expected))
        return super()._check_pos(expected)

    def test_init_and_set(self):
        
        self.assertEqual(mock_builtin.__pos__, [0, 0, 0])

        with self.subTest("set mapSize value"):
            mock_builtin.set_map_size(9)
            self.assertEqual(mock_builtin.__map_size__, 9)
            self.assertEqual(mock_builtin.get_world_size(), 9)

        for case in _POS_CASES:
            with self.subTest("set pos values", case = case):
                self._reset_pos()
                mock_builtin.set_pos(*case.args, **case.kwargs)
                self._check_pos(case.expected)
    def test_set_out_of_bounds(self):
        # Force this how I want it
        mock_builtin.__pos__ = [ 3, 3, 0]
        mock_builtin.set_map_size(10)
        for ob_case in [(-1, 5), (5, -3), (200, 3), (4, 1000), (-1, 5000), (209390, -923)]:
            with self.subTest(f"Checking that {ob_case} is out of bounds"):
                with self.assertRaises(ValueError, msg=f"should have raised value error. __pos__ is {mock_builtin.__pos__}") as ar:  # noqa: F841
                    mock_builtin.set_pos(*ob_case)
                self.assertEqual(mock_builtin.get_pos(), (3, 3, 0))


    def test_move(self):
        CASES_2X2 = [
            MoveCase((0, 1), North),
            MoveCase((1,0), East),
            MoveCase((0,1), South),
            MoveCase((1, 0), West)
        ]
        CASES_3X3 = [

            MoveCase((0, 1), North),
            MoveCase((1,0), East),
            MoveCase((0,2), South),
            MoveCase((2, 0), West),

            MoveCase((1, 2), North, (1, 1)),
            MoveCase((2, 1), East, (1, 1)),
            MoveCase((1, 0), South, (1, 1)),
            MoveCase((0, 1), West, (1, 1)),

            MoveCase((2, 0), North, (2, 2)),
            MoveCase((0, 2), East, (2, 2)),
            MoveCase((2, 1), South, (2, 2)),
            MoveCase((1, 2), West, (2, 2)),
        ]
        with self.subTest("2x2"):
            mock_builtin.set_map_size(2)
            for case in CASES_2X2:
                with self.subTest("2x2 move case", case=case):
                    case.run_case(self)

        with self.subTest("3x3"):
            mock_builtin.set_map_size(3)
            for case in CASES_3X3:
                with self.subTest("3x3 move case", case=case):
                    case.run_case(self)

_MoveCase = namedtuple("_MoveCase", ["expected", "direction", "origin"], defaults=[(0, 0)])
class MoveCase(_MoveCase):
    def run_case(self, test_case:BaseCase):
        mock_builtin.__pos__ = [self.origin[0], self.origin[1], 0]
        mock_builtin.move(self.direction)
        test_case.assertEqual(
            mock_builtin.__pos__, [self.expected[0], self.expected[1], 0])

