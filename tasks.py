



import memory
from __builtins__ import (
    Direction,
    East,
    Entities,
    Ground,
    Grounds,
    Items,
    North,
    South,
    West,
    can_harvest,
    get_entity_type,
    get_ground_type,
    get_hardness,
    get_stability,
    get_water,
    get_world_size,
    harvest,
    move,
    num_items,
    plant,
    quick_print,
    random,
    till,
    use_item,
)
from const import CARROT_MIN, DIRECTIONS
from util import (
    get_borders,
    opposite_direction,
    point_at_direction,
    print_map,
    resolve_x,
    resolve_y,
    update,
)

KEY_ENT = "Entity"
KEY_GROUND = "Ground"
KEY_STABILITY = "Stability"
KEY_HARDNESS = "Hardness"
KEY_TIME = "Time"

def do_observe(
        x=None, y=None, 
        surroundings: bool | list[Direction] = False,
        preset: dict | None = None, backoff_time: float = 2.0
    ) -> dict[tuple[int, int], tuple[Grounds, Entities, float, float, float, ]]:
    preset = preset or {}
    observed_here = {}

    x, y = resolve_x(x), resolve_y(y)
    entity = None
    ground = None
    stability = None
    hardness = None
    time = None
    #entity_val  = None
    if KEY_ENT in preset:
        entity = preset[KEY_ENT]
    #if entity_val != None:
    #	entity = Entities(entity_val)
    #ground_val = None
    if KEY_GROUND in preset:
        ground = preset[KEY_GROUND]
    #if ground_val != None:
    #	ground = Grounds(ground_val)
    #	if ground_val == None:
    #		ground = Grounds(ground_val)
    if KEY_STABILITY in preset:
        stability = preset[KEY_STABILITY]
    if KEY_HARDNESS in preset:
        hardness = preset[KEY_HARDNESS]
    if KEY_TIME in preset:
        time = preset[KEY_TIME]
    observed_here[(x, y)] = (ground, entity, stability, hardness, time)
    if not surroundings:
        update(memory.map, observed_here)
        print_map(memory.map)
        return observed_here
    elif surroundings == True:
        surroundings = [North, South, East, West]
    for neighbor in surroundings:
        if neighbor in get_borders(x, y):
            continue
        observed_here[point_at_direction(neighbor)] = (
            get_ground_type(neighbor),
            get_entity_type(neighbor),
            get_stability(neighbor),
            get_hardness(neighbor),
            time,
        )
        
    update(memory.map, observed_here)
    print_map(memory.map)
    return observed_here

def pay_attention(x, y, hyperattentive: float = 0.5, attentiveness: float = 1.0):
    
    if not 0.0 <= attentiveness <= 1.0:
        print(str(attentiveness) + " must be in between 0 and 1")
    if not 0.0 <= hyperattentive <= 1.0:
        print (str(hyperattentive) + " must be in between 0 and 1")
    if attentiveness == 1.0 or random() < attentiveness:
        do_observe(x, y, random() < hyperattentive)

    


def go_to(pos, x=None, y=None, tasks=None):
    if tasks == None:
        tasks = []
    x = resolve_x(x)
    y = resolve_y(y)
        
    if x > pos[0]:
        x_move = West
    else:
        x_move = East
    if y > pos[1]:
        y_move = South
    else:
        y_move = North
    
    for _ in range(abs(x-pos[0])):
        move(x_move)
        for task in tasks:
            task(x, y)
    for _ in range(abs(y-pos[1])):
        move(y_move)
        for task in tasks:
            task(x, y)



def interrupt(do, return_to, goto = None):
    if goto != None:
        go_to(goto)
    do()
    go_to(return_to)
    
def replace_rotten(direction, x=None, y=None, stay=False, goto=None):
    if get_entity_type(direction) == Entities.Dead_Pumpkin:
        rx, ry = point_at_direction(direction, x, y)
        move(direction)
        do_plant(rx, ry)
        do_replace_rotten(rx, ry, opposite_direction(direction), goto)
        if goto != None:
            quick_print("after replace_rotten, going to " + str(goto))
            go_to(goto)
        elif not stay:
            move(opposite_direction(direction))
        
def do_replace_rotten(x:int , y:int, travel: Direction | None = None, goto=None):
    if travel == None:
        travel = memory.last_direction
    if goto == None:
        goto = (x, y)
    for direction in DIRECTIONS:
        if direction == South and y == 0 or direction == North and y == get_world_size()-1 or direction == West and x == 0 or direction == East and x == get_world_size() -1:
            continue
        if direction != travel:
            replace_rotten(direction, x, y, False, goto)
    # always do direction of travel last
    if travel != None:
        replace_rotten(travel, x, y)

def buddy_up():
    return None

def do_harvest(_x: int =-1, _y: int = -1, max_harvest=70*7):
    here_harvested = 0
    while can_harvest():
        harvest()
        here_harvested += 1
        
        if here_harvested >= max_harvest or not can_harvest():
            break

def do_plant(x:int, y:int):
    to_plant = None
    hay = num_items(Items.Hay)
    wood = num_items(Items.Wood)
    ground_type: Ground | None = None
    if x == y or abs(x-y) % 2:
        ground_type = get_ground_type()
        if ground_type != Grounds.Soil:
            till()
        carrots = num_items(Items.Carrot)
        pumpkins = (num_items(Items.Pumpkin) or 0)
        
        if  carrots >= CARROT_MIN and carrots > pumpkins:
            to_plant = Entities.Pumpkin
        else:
            to_plant = Entities.Carrot
    elif hay > wood:
        to_plant = Entities.Tree
    while get_water() < 1.0 and num_items(Items.Water) > 0:
        use_item(Items.Water)
    if to_plant != None:
        plant(to_plant)
        #memory.set_cell_entity_and_ground(x, y, to_plant, memory.NO_MEMORY)
    return to_plant
