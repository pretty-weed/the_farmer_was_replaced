



from __builtins__ import (
    Callable,
    Direction,
    East,
    Entities,
    Grounds,
    Items,
    North,
    South,
    West,
    can_harvest,
    clear,
    dig,
    get_entity_type,
    get_ground_type,
    get_pos_x,
    get_pos_y,
    get_pos_z,
    get_world_size,
    harvest,
    move,
    num_items,
    plant,
    prospect_iron,
    quick_print,
)
from const import DIRECTIONS
from discover import find_surface_list
from movement import go_to, weave
from stdlib_patch import setdefault
from tasks import do_dig
from util import (
    all,
    bubble_sort,
    get_range_dict,
    opposite_direction,
    point_at_direction,
    reverse,
    union_update,
)

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


def mine_neighbor(
        direction: Direction, 
        x: int | None = None, y: int | None = None, z: int | None = None, 
        recursive=0, dug: dict[tuple[int,int], int] | None = None) -> dict[tuple[int, int], int]:
    
    if z == None:
        z = get_pos_z()
    if y == None:
        y = get_pos_y()
    if x == None:
        x = get_pos_x()
    move(direction)
    pos = (x, y)
    if dug == None:
        dug = {pos: 0}
    else:
        dug.setdefault(pos, 0)
    while get_pos_z() > z:
        dig()
        dug[pos] += 1
        if recursive > 0:
            for rdir in DIRECTIONS:
                x, y = point_at_direction(rdir, x, y)
                mine_neighbor(rdir, x, y, z, recursive-1)
    move(opposite_direction(direction))
    return dug

def clear_rice_terrace():

    cleared = [False]
    def do_clear(_x, _y):
        for _ in range(2):
            if get_ground_type() != Grounds.Dry_Rice_Terrace:
                break
            dig()

        cleared.append(get_ground_type() != Grounds.Dry_Rice_Terrace)
    
    while not all(cleared):
        cleared = []
        weave([(1.0, [], do_clear)])


def farm_rice():
    global done_digging
    done_digging = False
    def check_and_dig_or_farm(x, y):

        global done_digging
        ent_here = get_entity_type()
        if get_ground_type() in [Grounds.Clay, Grounds.Rice_Terrace] or ent_here == Entities.Rice:
            if done_digging == (x, y):
                # came around
                done_digging = True
            elif done_digging == False:
                done_digging = (x, y)
                
            if ent_here == None:
                plant(Entities.Rice)
        else:
            i = 0
            while i < 3:
                dig()
                if get_ground_type() == Grounds.Clay:
                    plant(Entities.Rice)
                    break
                i += 1

    def done_cond():
        return done_digging != True
    while done_digging != True:
        go_to((get_world_size()/2, 0))
        weave([(1.0, [], check_and_dig_or_farm)])
    
    def do_harvest(_x, _y):
        while not can_harvest():
            pet_the_piggy()
        harvest()
    weave([(1.0, [], do_harvest)])

    clear_rice_terrace()




# might optimize by returning tuple[tuple[int, int] | None, Direction | None], 
# or something else to differrentiate those that are immediately adjacent
def handle_spot(spot: tuple[int, int], dig_neighbors=3, 
    to_mine=(Grounds.Coal, Grounds.Iron)) -> list[tuple]:
    go_to(spot)
    dig()
    new_spots = []
    while get_ground_type() in to_mine:
        dig()
        for direction in [North, East, South, West]:
            dir_ground = get_ground_type(direction)
            if dir_ground in to_mine:
                dp = point_at_direction(direction, spot[0], spot[1])
                if dig_neighbors:
                    for new_spot in mine_neighbor(direction, get_pos_z(), dig_neighbors):
                        new_spots.append(new_spot)
                else:
                    new_spots.append(dp)
    return new_spots

def z_prioritize_resource(found: dict[tuple[int, int], int]):
    res_by_z = {}
    for pos in found:
        setdefault(res_by_z, found[pos], []).append(pos)
    sorted_zs = reverse(bubble_sort(res_by_z))
    prioritized = []
    for z in sorted_zs:
        dists = get_range_dict(res_by_z[z])
        # picking first min is kinda arbitrary but meh
        sorted_dists = bubble_sort(dists)
        for dist in sorted_dists:
            prioritized += dists[dist]
    quick_print("prioritized:" + str(prioritized))
    return prioritized

def mine_coal(max_coal: int=COAL_MAX_THRESHOLD, min_loops: int = 1, keep_clay:bool = True):
    coal_spots: dict[tuple[int, int], int] = {}
    ignore_spots = set()
    loops = 0
    while num_items(Items.Coal) < max_coal or loops < min_loops:
        loops += 1
        found = find_surface_list(
            [Grounds.Coal, Grounds.Clay, Grounds.Rice_Terrace, Grounds.Dry_Rice_Terrace], [],
            True, ignore_spots)
        if found:
            if Grounds.Coal in found:
                coal_spots = found[Grounds.Coal]
            for clay_type in [Grounds.Clay, Grounds.Dry_Rice_Terrace, Grounds.Rice_Terrace]:
                    if clay_type in found:
                        # ToDo maybe ignore spots around if they're not in coal
                        union_update(ignore_spots, found[clay_type])
            
            
        new_spots = []
        rem_to_check = z_prioritize_resource(coal_spots)
        if rem_to_check:
            quick_print("found coal: ", rem_to_check)
        else:
            quick_print("found no coal")
        while rem_to_check:
            next_spot = rem_to_check.pop(0)
            for new_spot in handle_spot(next_spot, 3):
                new_spots.append(new_spot)
            
            if not rem_to_check:
                found = find_surface_list(
                    [Grounds.Coal])
                if found:
                    rem_to_check = z_prioritize_resource(found[Grounds.Coal])
        conditions = []
        def no_dig_clay():
            if get_ground_type() in [Grounds.Clay, Grounds.Rice_Terrace, Grounds.Dry_Rice_Terrace]:
                return False
            return (get_pos_x(), get_pos_y()) not in ignore_spots

        if keep_clay:
            conditions.append(no_dig_clay)
        world_size = get_world_size()
        skip= 2
        if loops % 2:
            offset_base = world_size % (skip+1)
            offset = (offset_base, offset_base)
        else:
            offset = (0, 0)
        quick_print("weave " + str(loops) + " offset " + str(offset))
        weave([(1.0, conditions, do_dig)], True, skip, offset)
        

                    

def continue_func_factory(min_coal=COAL_MIN_THRESHOLD, max_depth: int | None = None, max_iterations: int | None = None) -> Callable:

    def continue_func(iteration: int, coal: int = min_coal, depth=max_depth, iterations=max_iterations):
        return num_items(Items.Coal) < coal and (iterations == None or iteration <= iterations) and (depth == None or get_pos_z() >= depth) 

    return continue_func

def mine_iron(min_coal = COAL_MIN_THRESHOLD, coal_interval_z:int = 15):
    world_size = get_world_size()
    center = world_size // 2
    # Move to center
    x: int = get_pos_x()
    y: int = get_pos_y()
    while True:
        while num_items(Items.Coal) < min_coal:
            mine_coal(min_coal * 2)
        go_to((center, center))
        prospect_here = 0
        while num_items(Items.Coal) >= min_coal:

            prospect: Direction = prospect_iron()
            quick_print("prospect result: ", prospect)
            while prospect == None:
                while get_ground_type() != Grounds.Iron:
                    prospect_here += 1
                    dig()
                while get_ground_type() == Grounds.Iron:
                    dig()
                prospect = prospect_iron()
                if prospect_here > coal_interval_z:
                    mine_coal(min_coal * 2, 1)
                prospect_here =0
            move(prospect)
        

def main_scrape():
    clear()
    #weave([(1.0, [], do_harvest)], True)
    
    while True:
        weave([(1.0, [], do_dig)], False, 1)



def main(clearme=True, reset_pos=True,miner=farm_rice):
    if reset_pos:
        go_to((0, 0))
    if clearme:
        clear()
    miner()


if __name__ == "__main__":
    main()