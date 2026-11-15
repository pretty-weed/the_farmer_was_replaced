from typing import TypeAlias
from unittest import mock

from __builtins__ import Direction as Direction
from __builtins__ import East as East
from __builtins__ import Entities as Entities
from __builtins__ import Entity as Entity
from __builtins__ import Ground as Ground
from __builtins__ import Grounds as Grounds
from __builtins__ import Item as Item
from __builtins__ import Items as Items
from __builtins__ import North as North
from __builtins__ import South as South
from __builtins__ import Unlock as Unlock
from __builtins__ import Unlocks as Unlocks
from __builtins__ import West as West
from __builtins__ import string


def _dir_name(direction: Direction) -> string:
    return {
        North: "North",
        East: "East",
        South: "South",
        West: "West"
    }[direction]

_mocks = {}
__map_size__ = 12
__pos__: list[int, int, int] = [0, 0, 0]

_x = 0
_y = 1
_z = 2

optionalInt: TypeAlias = int | None

_SETUP_ARGS = {
    "move": (East,)
}

def mock_builtin(side_effect):
    to_mock = side_effect.__name__.strip("_")
    _mocks[to_mock] = mock.MagicMock(name=f"mock_builtin.{to_mock}", spec=side_effect)
    _mocks[to_mock].side_effect = side_effect
    return side_effect

@mock_builtin
def __get_world_size__() -> int:
    return __map_size__

@mock_builtin
def __get_pos_x__() -> int:
    return __pos__[_x]

@mock_builtin
def __get_pos_y__() -> int:
    return __pos__[_y]

@mock_builtin
def __get_pos_z__() -> int:
    return __pos__[_z]

@mock_builtin
def __quick_print__(*vals):
    print(*vals)

def __getattr__(name: string):
    if name not in _mocks:
        _mocks[name] = mock.MagicMock(name=f"mock_builtin.{name}")
    return _mocks[name]

def reset_all():
    """Helper to clear call history between tests."""
    for mock in _mocks.values():
        mock.reset_mock()
    global __pos__
    __pos__ = [0, 0, 0]

@mock_builtin
def __move__(direction: Direction, /) -> bool:
    pos = get_pos()
    if direction == North:
        if pos[_y] == __map_size__-1:
            set_pos(y=0)
        else:
            set_pos(y=__pos__[_y] + 1)
    elif direction == East:
        if pos[_x] == __map_size__-1:
            set_pos(x=0)
        else:
            set_pos(x=__pos__[_x] + 1)
    elif direction == South:
        if pos[_y] == 0:
            set_pos(y=__map_size__-1)
        else:
            set_pos(y=__pos__[_y]-1)
    elif direction == West:
        if pos[_x] == 0:
            set_pos(x=__map_size__-1)
        else:
            set_pos(x=__pos__[_x]-1)
    else:
        raise TypeError(f"{direction} is not a Direction")
    
    return True

def set_map_size(size: int):
    global __map_size__ 
    __map_size__ = size

def get_pos()-> tuple[int, int, int]:
    return tuple[int, int, int](__pos__)

def set_pos(x: optionalInt = None, y: optionalInt = None, z: optionalInt = None) -> tuple[int, int, int]:
    msg = ""
    if x is not None:
        x_low, x_high = x < 0, x >= __map_size__
        if x_low:
            msg += f"X is too small ({x})"
        elif x_high:
            msg += f"X is too large({x}>={__map_size__})"
    if y is not None:
        y_low, y_high = y < 0, y >= __map_size__
        if y_low:
            msg += f"Y is too small ({y})"
        elif y_high:
            msg += f"Y is too large({y}>={__map_size__})"

    
    if msg:
        raise ValueError(msg)
    if x is not None:
        __pos__[0] = x
    if y is not None:
        __pos__[1] = y
    if z is not None:
        __pos__[2] = z
    
    
    
    return get_pos()







