
from __builtins__ import (
    Callable,
    Direction,
    East,
    Grounds,
    Items,
    North,
    South,
    West,
    clear,
    dig,
    get_ground_type,
    get_pos_x,
    get_pos_y,
    get_pos_z,
    get_world_size,
    move,
    num_items,
    prospect_iron,
    quick_print,
)
from const import DIRECTIONS
from movement import go_to, weave
from tasks import do_dig
from util import get_range_dict, opposite_direction, point_at_direction

COAL_MIN_THRESHOLD = 25
COAL_MAX_THRESHOLD = 125


def find_surface_map(grounds=None):
    if grounds == None:
        grounds = [Grounds.Coal, Grounds.Iron]
    found = {}
    def check_cell(x, y):
        ground = get_ground_type()
        if ground in grounds:
            if ground not in found:
                found[ground] = {}
            found[ground][(x, y)] = True
    
    weave([(1.0, [], check_cell)])
    return found

def find_surface_list(grounds=None, reset=False):
    if grounds == None:
        grounds = [Grounds.Coal, Grounds.Iron]
    found = {}
    def check_cell(x, y):
        ground = get_ground_type()
        if ground in grounds:
            if ground not in found:
                found[ground] = []
            found[ground].append((x, y))
    
    weave([(1.0, [], check_cell)], reset)
    return found

def mine_neighbor(direction: Direction, z: int | None = None, recursive=0):
    if z == None:
        z = get_pos_z()
    move(direction)
    dug = 0
    while get_pos_z() > z:
        dig()
        dug += 1
        if recursive > 0:
            for rdir in DIRECTIONS:
                dug += mine_neighbor(rdir, z, recursive-1)
    move(opposite_direction(direction))
    return dug

# might optimize by returning tuple[tuple[int, int] | None, Direction | None], 
# or something else to differrentiate those that are immediately adjacent
def handle_spot(spot: tuple[int, int], dig_neighbors=3) -> list[tuple]:
    go_to(spot)
    dig()
    new_spots = []
    while get_ground_type() == Grounds.Coal:
        dig()
        for direction in [North, East, South, West]:
            dir_ground = get_ground_type(direction)
            if dir_ground == Grounds.Coal:
                dp = point_at_direction(direction, spot[0], spot[1])
                if dig_neighbors:
                    for new_spot in mine_neighbor(direction, get_pos_z(), dig_neighbors):
                        new_spots.append(new_spot)
                else:
                    new_spots.append(dp)
    return new_spots

def mine_coal(max_coal: int=COAL_MAX_THRESHOLD, min_loops: int = 1):
    coal_spots = []
    loops = 0
    while num_items(Items.Coal) < max_coal and loops < min_loops:
        loops += 1
        found = find_surface_list([Grounds.Coal], True)
        if found:
            coal_spots = found[Grounds.Coal]
        new_spots = []
        rem_to_check = coal_spots
        if rem_to_check:
            quick_print("found coal: ", rem_to_check)
        else:
            quick_print("found no coal")
        while rem_to_check:
            quick_print("remaining to check:", rem_to_check)
            rem_ranges = get_range_dict(rem_to_check)
            # picking first min is kinda arbitrary but meh
            nearest = rem_ranges[min(rem_ranges)][0]
            rem_to_check.remove(nearest)
            for new_spot in handle_spot(nearest, 3):
                new_spots.append(new_spot)
            
            if not rem_to_check:
                found = find_surface_list([Grounds.Coal])
                if found:
                    rem_to_check = found[Grounds.Coal]

        weave([(1.0, [], do_dig)], True, 2)
                    

def continue_func_factory(min_coal=COAL_MIN_THRESHOLD, max_depth: int | None = None, max_iterations: int | None = None) -> Callable:

    def continue_func(iteration: int, coal: int = min_coal, depth=max_depth, iterations=max_iterations):
        return num_items(Items.Coal) < coal and (iterations == None or iteration <= iterations) and (depth == None or get_pos_z() >= depth) 

    return continue_func

def mine_iron(min_coal = COAL_MIN_THRESHOLD, coal_interval_z:int = 5):
    world_size = get_world_size()
    center = world_size // 2
    # Move to center
    x: int = get_pos_x()
    y: int = get_pos_y()
    while True:
        while num_items(Items.Coal) < min_coal:
            mine_coal(min_coal * 2)
        go_to((center, center), (x, y))
        prospect_here = 0
        while num_items(Items.Coal) < min_coal:

            prospect: Direction = prospect_iron()
            quick_print("prospect result: ", prospect)
            if prospect == None:
                prospect_here += 1
                dig()
                if prospect_here > coal_interval_z:
                    mine_coal(min_coal * 2, 1)
                prospect_here =0
            else:
                move(prospect)
        

def main_scrape():
    clear()
    #weave([(1.0, [], do_harvest)], True)
    
    while True:
        weave([(1.0, [], do_dig)], False, 1)



def main(clearme=True, miner=mine_iron):
    if clearme:
        clear()
    miner()


if __name__ == "__main__":
    main()