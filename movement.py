# movement.py
from __builtins__ import (
    Any,
    Callable,
    Direction,
    East,
    North,
    South,
    West,
    WorldSizes,
    get_pos_x,
    get_pos_y,
    get_world_size,
    int,
    move,
    quick_print,
)


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
    reset=False, skip=0, offset=0):
    world_size: WorldSizes = get_world_size()
    even_world = world_size % 2 == 0
    world_end = world_size -1
    if reset:
        while get_pos_x():
            move(East)
        while get_pos_y():
            move(South)
    elif skip:
        while get_pos_x() % (skip + 1):
            move(East)
    step_moves = skip+1
    counter = 0
    if skip:
        cycle_end = world_end - (world_end % skip)-1
    else:
        cycle_end = world_end
    # quick_print("range confs:", "offset", "world_size", "step_moves", "cycle end")
    x_step=-1
    orig_x = get_pos_x()
    orig_y = get_pos_y()
    for x in range(offset, world_size, step_moves): 
        x_step += 1
        y_step =-1
        for y in range(offset, world_size, step_moves ):
            y_step += 1
            px = get_pos_x()
            py = get_pos_y()

            travel = []
            if px == cycle_end and (( even_world and py == 0) or (not even_world and py == cycle_end)):
                quick_print("far right end corner")
                if not even_world:
                    
                    for _ in range(cycle_end):
                        travel.append(South)
                for _ in range(cycle_end):
                    travel.append(West)
                    
            elif (x_step % 2 and py == 0) or (not(x_step % 2) and py == cycle_end):
                c1_res = (x_step % 2 and py == 0)
                c2_res = (not(x_step % 2) and py == cycle_end)
                # quick_print("East cond res:: c1:", c1_res, ", c2:", c2_res)
                
                # if c1_res and c2_res:
                    # quick_print("adding ", step_moves, "moves", East, "because both true")
                # elif c1_res:
                    # quick_print("adding ", step_moves, "moves", East, "because even x and at bottom")
                # elif c2_res:
                    # quick_print("adding ", step_moves, "moves", East, "because odd x and at top")
                travel = n_moves(East, step_moves)
            elif x_step % 2:
                # quick_print("adding ", step_moves, "moves", South)
                travel = n_moves(South, step_moves)
            else:
                # quick_print("adding ", step_moves, "moves", North)
                travel = n_moves(North, step_moves)
            
            for task in tasks:
                handle_task(task, counter, px, py)
            for t in travel:
                move(t)

            counter += 1

def handle_task(task, counter, x, y):
    period, conditions, task_do = task
    if not counter % period:
        for condition in conditions:
            if not condition():
                return 
        task_do(x, y)



