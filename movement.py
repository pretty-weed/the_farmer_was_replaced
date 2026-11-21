# movement.py
from log_conf import setup_logging

LOGGER = setup_logging(__name__)
LOGGER.setLevel(0)
from __builtins__ import (
    Any,
    Callable,
    Direction,
    East,
    North,
    South,
    West,
    get_pos_x,
    get_pos_y,
    get_world_size,
    int,
    move,
)
from stdlib_patch import setdefault
from util import any, floor


def n_moves(direction: Direction, n: int = 1) -> list[Direction]:
    res = []
    for _ in range(n):
        res.append(direction)
    return res

def go_to(target: tuple[int, int], origin: tuple[int, int] | None = None)-> int:
    if origin == None:
        origin = (get_pos_x(), get_pos_y())
    steps = 0
    if target[0] > origin[0]:
        h_dir = East
    else:
        h_dir = West
    if target[1] > origin[1]:
        v_dir = North
    else:
        v_dir = South
    v_steps = n_moves(v_dir, abs(target[1]-origin[1]))
    h_steps = n_moves(h_dir, abs(target[0]-origin[0]))
    for step in v_steps + h_steps:
        move(step)
    return len(v_steps) + len(h_steps)


# period (do 1 / every n), conditions, callable
def weave(
    tasks:list[tuple[float, list[Callable[[],Any]], Callable[[int, int], Any]]],
    reset=False, skip=0, offset=(0, 0), size: int | None = None):
    if size == None:
        size = get_world_size()
    num_paths = floor(size / (skip + 1)) + (size % (skip+1) )
    even_paths = num_paths  % 2 == 0
    world_end = size -1

    if reset:
        while get_pos_x():
            move(East)
        while get_pos_y():
            move(South)

    if any(offset):
        LOGGER.info('moving to offset %s',offset)
        for off_x in range(abs(offset[0])):
            if offset[0] > 0:
                move(East)
            else:
                move(West)
        for _ in range(abs(offset[1])):
            if offset[1] > 0:
                move(North)
            else:
                move(South)
        LOGGER.info('moved to offset')
    elif skip:
        while get_pos_x() % (skip + 1):
            move(East)
    step_moves = skip+1
    counter = 0
    if skip:
        cycle_end_base = world_end - (world_end % step_moves) 
    else:
        cycle_end_base = world_end
    if offset:
        cycle_end_x = cycle_end_base + offset[0]
        cycle_end_y = cycle_end_base + offset[1]
    else:
        cycle_end_x = cycle_end_base
        cycle_end_y = cycle_end_base
    x_step: int =-1
    y_step: int =-1
    orig_x: int = get_pos_x()
    orig_y: int = get_pos_y()
    prev_cycle: tuple[int, int] = (-1, -1)
    px: int = orig_x
    py: int = orig_y
    prev_move: None | dict[str, int] = None
    LOGGER.info("weave config:")
    LOGGER.info("offset: %s, world_size: %s, skip: %s, step_moves: %s cycle_ends: %s", offset, size, skip, step_moves, (cycle_end_x, cycle_end_y))
    # TOREMOVE for debugging/work
    previous: list[dict[str, Any]] = []
    for x in range(offset[0], size, step_moves): 
        prev_steps: tuple[int, int] = (x_step, y_step)
        x_step += 1
        y_step = -1
        if x_step % 2:
            # removed a -1
            y_range_start = cycle_end_y 
            y_range_end = offset[1] -1
            range_steps = -step_moves
        else:
            y_range_start = offset[1]
            y_range_end = size
            range_steps = step_moves
        _tpy = get_pos_y()
        # assert _tpy == y_range_start
        for y in range(y_range_start, y_range_end, range_steps):
            this_previous = {
                "cycle": prev_cycle,
                "pos": (px, py),
                "move": prev_move,
                "steps": prev_steps,
            }
            previous.append(this_previous)
            px = get_pos_x()
            py = get_pos_y()
            # assert  px == x and py == y
            y_step += 1
            LOGGER.debug("x range[%d]: %s", x, list(range(offset[0], size, step_moves)))
            LOGGER.debug("y range[%d]: %s", y, list(range(y_range_start, y_range_end, range_steps)))
            LOGGER.info("loop: x/y: %s, px/py: %s, steps: %s", (x, y), (px, py), (x_step, y_step))
            LOGGER.debug("Go east: x_step (%d) is odd and py (%d) == 0 OR  x_step (%s) is even (%s) and py (%s) == %s", 
                x_step, py, x_step, not (x_step % 2), py, cycle_end_y)
            travel = []
            # TOREMOVE previous stuff is for debugging
            prev_move = {} 
            if x_step == y_step == num_paths-1:
                LOGGER.debug("at final corner: %s", (px, py))
                if not even_paths:
                    setdefault(prev_move, "South", 0)
                    prev_move["South"] += py
                    for _ in range(y):
                        travel.append(South)
                for _ in range(cycle_end_x):
                    setdefault(prev_move, "West", 0)
                    prev_move["West"] += cycle_end_x
                   
                    travel.append(West)
                    
            elif (x_step % 2 and y == offset[1]) or (not(x_step % 2) and y == cycle_end_y):
                c1_res = (x_step % 2 and y == offset[1])
                c2_res = (not(x_step % 2) and y == cycle_end_y)
                if c1_res and c2_res:
                    LOGGER.info("adding %d moves East because both true", step_moves,)
                elif c1_res:
                    LOGGER.info("adding %d moves East because even x and at bottom", step_moves)
                elif c2_res:
                    LOGGER.info("adding %d moves East because odd x and at top", step_moves)
                setdefault(prev_move, "East", 0)
                prev_move["East"] += step_moves
                
                travel = n_moves(East, step_moves)
            elif x_step % 2:
                _tpy = get_pos_y()
                #assert _tpy >= offset[1] + step_moves
                setdefault(prev_move, "South", 0)
                prev_move["South"] += step_moves
                
                LOGGER.info("adding %d moves South because on odd vertical", step_moves)
                travel = n_moves(South, step_moves)
            else:
                setdefault(prev_move, "North", 0)
                prev_move["North"] += step_moves

                LOGGER.info("adding %d moves North because on even vertical", step_moves)
                travel = n_moves(North, step_moves)
            
            for task in tasks:
                handle_task(task, counter, px, py)
            for t in travel:

                move(t)
            prev_cycle = (x, y)
            counter += 1

def handle_task(task, counter, x, y):
    period, conditions, task_do = task
    if not counter % period:
        for condition in conditions:
            if not condition():
                return 
        task_do(x, y)



    