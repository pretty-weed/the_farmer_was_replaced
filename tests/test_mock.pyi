from typing import NamedTuple

class SetPosCase(NamedTuple):
    x: int
    y: int
    expected: bool


class MoveCase(NamedTuple):
    expected: tuple[int, int]
    direction: mock_builtin.Direction
    origin: tuple[int, int] = (0, 0)