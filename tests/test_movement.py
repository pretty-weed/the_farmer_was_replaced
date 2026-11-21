

from .base_test import *  # noqa: I001
# must come after base test import
import movement


class TestWeave(BaseCase):
    def _get_do_check(self, positions):
        check_positions = iter(positions)
        def do_check(x, y):
            expected = next(check_positions)
            self._check_pos(expected)
        return do_check
    def test_3(self):
        self._set_map_size(3)
        check_positions = [
            (0, 0, 0),
            (0, 1, 0),
            (0, 2, 0),
            (1, 2, 0),
            (1, 1, 0),
            (1, 0, 0),
            (2, 0, 0),
            (2, 1, 0),
            (2, 2, 0),
        ]
        movement.weave([(1.0, [], self._get_do_check(check_positions))])
        self._check_pos((0,0,0))
    
    def test_4(self):
        self._set_map_size(4)
        check_positions = [
            (0, 0, 0),
            (0, 1, 0),
            (0, 2, 0), 
            (0, 3, 0),
            (1, 3, 0),
            (1, 2, 0),
            (1, 1, 0),
            (1, 0, 0),
            (2, 0, 0),
            (2, 1, 0),
            (2, 2, 0),
            (2, 3, 0),
            (3, 3, 0),
            (3, 2, 0),
            (3, 1, 0),
            (3, 0, 0)
        ]
        
        movement.weave([(1.0, [], self._get_do_check(check_positions))])
        self._check_pos((0, 0, 0), "final cycle check")
    def test_offset(self):
        self._set_map_size(9)
        path = [
            (0, 0, 0),
            (0, 3, 0),
            (0, 6, 0),
            (3, 6, 0),
            (3, 3, 0),
            (3, 0, 0),
            (6, 0, 0),
            (6, 3, 0),
            (6, 6, 0),
        ]
        offset = 1
        offset_path = [(x+offset, y+offset, z) for x, y, z in path]
        movement.weave([(1.0, [], self._get_do_check(path))], True, 2)
        self._check_pos((0, 0, 0), "final cycle check: unoffset")
        movement.weave([(1.0, [], self._get_do_check(offset_path))], False, 2, (offset, offset))
        self._check_pos((0, 0, 0), "final cycle check: offset")

    def test_offset_and_ws_change(self):
        self._set_map_size(10)
        path = [
            (0, 0, 0),
            (0, 3, 0),
            (0, 6, 0),
            (0, 9, 0),
            (3, 9, 0),
            (3, 6, 0),
            (3, 3, 0),
            (3, 0, 0),
            (6, 0, 0),
            (6, 3, 0),
            (6, 6, 0),
            (6, 9, 0),
            (9, 9, 0),
            (9, 6, 0),
            (9, 3, 0),
            (9, 0, 0),
        ]
        offset = 1
        offset_path = [(x+offset, y+offset, z) for x, y, z in path if x < 9 and y < 9]
        movement.weave([(1.0, [], self._get_do_check(path))], 
        True, 2)
        self._check_pos((0, 0, 0), "final cycle check: unoffset")
        
        movement.weave([(1.0, [], self._get_do_check(offset_path))],
         False, 2, (offset, offset), 9)
        self._check_pos((0, 0, 0), "final cycle check: offset")


    def test_skip(self):
        self._set_map_size(10)
        cases = {
            1: [
                (0, 0, 0),
                (0, 2, 0),
                (0, 4, 0),
                (0, 6, 0),
                (0, 8, 0),
                (2, 8, 0),
                (2, 6, 0),
                (2, 4, 0),
                (2, 2, 0),
                (2, 0, 0),
                (4, 0, 0),
                (4, 2, 0),
                (4, 4, 0),
                (4, 6, 0),
                (4, 8, 0),
                (6, 8, 0),
                (6, 6, 0),
                (6, 4, 0),
                (6, 2, 0),
                (6, 0, 0),
                (8, 0, 0),
                (8, 2, 0),
                (8, 4, 0),
                (8, 6, 0),
                (8, 8, 0)
            ],
            2: [
                (0, 0, 0),
                (0, 3, 0),
                (0, 6, 0),
                (0, 9, 0),
                (3, 9, 0),
                (3, 6, 0),
                (3, 3, 0),
                (3, 0, 0),
                (6, 0, 0),
                (6, 3, 0),
                (6, 6, 0),
                (6, 9, 0),
                (9, 9, 0),
                (9, 6, 0),
                (9, 3, 0),
                (9, 0, 0),
            ]
        }

        for skip, expected_points in cases.items():
            with self.subTest(skip=skip):
                movement.weave([(1.0, [], self._get_do_check(expected_points))], True, skip)
                self._check_pos((0, 0, 0), "finally cycle skip check")