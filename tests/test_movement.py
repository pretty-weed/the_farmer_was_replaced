

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
        self._check_pos((0, 0, 0))