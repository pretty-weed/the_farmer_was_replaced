from __builtins__ import (
    Any,
    Direction,
    East,
    Entities,
    Entity,
    Grounds,
    Item,
    North,
    South,
    West,
    _int,
    get_pos_x,
    get_pos_y,
    get_world_size,
    num_items,
    quick_print,
    random,
    string,
)
from const import ENT_RENDER, ENTITIES, ITEMS
from stdlib_patch import index, sum, zip


def floor(val: float) -> float:
    return val - (val % 1.0)

def enumerte(to_enum: list | dict | tuple) -> list:
    i = 0
    res =  []
    for val in to_enum:
        res.append((i, val))
        i += 1
    return res

def reverse(to_reverse: list | tuple) -> list:
    reversed = []
    for i in range(len(to_reverse)-1, -1, -1):
        reversed.append(to_reverse[i])
    return reversed

def bubble_sort(to_sort: list | dict | tuple | set, key=None):
    vals_to_sort = list(to_sort)
    n = len(vals_to_sort)
    if key == None:
        def key(val):
            return val
    for i in range(n):
        swapped = False
        
        # Last i elements are already in place, so we don't need to check them
        for j in range(n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if not yet sorted
            if key(vals_to_sort[j]) > key(vals_to_sort[j + 1]):
                vals_to_sort[j], vals_to_sort[j + 1] = vals_to_sort[j + 1], vals_to_sort[j]
                swapped = True
                
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break
    return vals_to_sort


def union(a, other, others=None):
    new = set()
    here_others = [other]
    if others:
        here_others += others
    union_update(new, a, here_others)
    return new

def multiunion(sets) -> set[Any]:
    return union([], [], sets)

def union_update(a, other, others=None):
    for item in other:
        a.add(item)
    if others:
        for additional_other in others:
            for item in additional_other:
                a.add(item)




def all(to_check) -> bool:
    for item in to_check:
        if not item:
            return False
    return True

def any(to_check) -> bool:
    for item in to_check:
        if item:
            return True
    return False


def update(da: dict, db: dict) -> None:
    for key in db:
        da[key] = db[key]

def item_to_entities(item: Item) -> set[Entity]:
    return ITEMS[item]

def entity_to_item(entity: Entity) -> Item:
    return ENTITIES[entity]

def resolve_entities(e_or_i: Item | Entity) -> set[Entity]:
    if e_or_i in ITEMS:
        return ITEMS[e_or_i]
    return set([e_or_i])

def resolve_x(x) -> _int:
    if x == None:
        return get_pos_x()
    return x

def resolve_y(y) -> _int:
    if y == None:
        return get_pos_y()
    return y

REMAINING = 1
ALLOCATED = 2
TOTAL = 3

def first_sort_key(item: list | tuple) -> Any:
    return item[0]

def _all_one_el(buckets: list[tuple[int, int, list[Any]]]):

    for bucket in buckets:
        if len(bucket[2]) != 1:
            return False

    return len(buckets) > 0

def distribute_greedy(vals: list[tuple[_int, Any]], bucket_count: _int) -> list[dict[string, Any]]:
    if bucket_count < 1:
        # invalid input, raise an error
        return [[(5/0, None)]]
    buckets: list[dict[string, int | list[Any]]] = []
    sums = []

    if len(vals) <= bucket_count:
        for i in range(len(vals)):
            size, item = vals[i]
            buckets.append({"s":size,"i": i,"e": [item]})
            sums.append(vals[i])
        return buckets

    at_zero = list(range(bucket_count))
    min_idx = -1
    for size, item in reverse(bubble_sort(vals, first_sort_key)):
        if at_zero:
            idx = at_zero.pop(0)
            buckets[idx] = {"s":size,"i": idx,"e": [item]}
            sums[idx] = size
            continue
        
        elif _all_one_el(buckets):
            min_idx = bucket_count

        buckets[min_idx][2].append((size, item))
        sums[min_idx] += size
        min_idx = index(sums, min(sums))
    return buckets

def random_choice(items: list[Any], weights: list[float] | None = None, abnormal_tolerance=0.1) -> Any:
    # force to a list
    items = list(items)
    if weights == None:
        weights = []
        for _ in range(len(items)):
            weights.append(1.0/len(items))
    cutoffs = []
    for weight in weights:
        cutoffs.append(sum(cutoffs) + weight)
    imbalance = abs(sum(weights) - 1.0)
    if imbalance > abnormal_tolerance:
        _weights = weights
        weights = []
        for weight in _weights:
            weights.append(weight *(1-imbalance))
    cursor = 0.0
    chosen = random()
    for i in range(len(items)):
        if cutoffs[i] >= chosen:
            return items[i]
    _ = 4/0


def _area_key(a: tuple[_int, _int], b: tuple[_int, _int] = (0, 0)):

    if a[0] > b[0] and a[1] > b[1]:
        bl = b
        tr = a
    elif a[0] < b[0] and a[1] < b[1]:
        bl = a
        tr = b
    else:
        print("Invalid to have wibbly points!")
        _ = 256/0

    return (tr[0]-bl[0])*(tr[1]-bl[1])

# 0 = x, 1 = y
def get_split_axis(area: tuple[_int, _int]) -> _int:
    if area[0] > area[1]:
        return 0
    elif area[0] < area[1]:
        return 1
    return random() > 0.5

def find_areas(weights: list[_int], area: tuple[_int, _int]) -> list[tuple[tuple[_int, _int], tuple[_int, _int], _int]]:
    weights = bubble_sort(weights)
    # bottom left (minx, miny), top right (maxx, maxy), entities
    areas: list[dict[string, Any]] = [{'bl':(0, 0), 'tr': area, 'it': list(range(len(weights)))}]
    quick_print("areas")
    quick_print(areas)
    quick_print("weights")
    quick_print(weights)
    while len(areas) < len(weights):
        quick_print("areas")
        quick_print(areas)
        quick_print("weights")
        quick_print(weights)
        areas = bubble_sort(areas, _area_key)
        # split up largest area
        to_split = -1
        while len(areas[to_split]) < 2:
            to_split -= 1
        bl, tr, here_items = areas.pop(to_split)
        weighted_indices: list[tuple[_int, _int]] =[]
        for item_idx in here_items:
            weighted_indices.append((weights[item_idx], item_idx))
        new_areas : list[tuple[tuple[_int, _int], tuple[_int, _int]]] = []
        if get_split_axis((tr[0]-bl[0], tr[1]-bl[0])):
            # split on y
            new_areas = [
                (bl, (tr[0], (tr[1]-bl[1])/2)),
                ((bl[0], (tr[1]-bl[1])/2), tr)
            ]
        else:
            # split on x
            new_areas = [
                (bl, ((tr[0]-bl[0])/2, tr[1])),
                (((tr[0]-bl[0])/2, bl[1]), tr)    
            ]
        # this_split_items: tuple[_int, _int] (weight, item_idx)
        for this_split_items, new_area in  zip(
                distribute_greedy(weighted_indices, 2),
                new_areas):
            areas.append({'bl': new_area[0], 'tr':new_area[1], 'it':this_split_items})
    
    final_areas = []
    for this_area in areas:
        if len(this_area[2]['e']) != 1:
            print("every area should have exactly 1 item")
            quick_print(this_area[2])
            print(14/0)
        final_areas.append((this_area[0], this_area[1], this_area[2]['e'][0]))
    return final_areas

def ent_to_item_count(ent: Entity) -> _int:
    quick_print('getting count of ent ' + str(ent))
    quick_print('getting count of ent item ' + str(ENTITIES[ent]))
    return num_items(ENTITIES[ent])

def ent_to_item_and_count(ent: Entity) -> tuple[Item, _int]:
    item = ENTITIES[ent]
    return (item, num_items(item))

    

def _sort_groups(groups: list[_int], area: tuple[_int, _int], sort_by: list[_int] = (REMAINING, ALLOCATED)):
    sort_tuples = []
    sub_areas = []
    for group_i in range(len(groups)):
        sub_areas.append([])
        sort_key = []
        for element in sort_by:
            abs_el = abs(element)
            if abs_el == element:
                maybe_negate = 1
            else:
                maybe_negate = -1
            if abs_el == REMAINING:
                _ = 1/0
                #sort_key.append()
            elif abs_el == ALLOCATED:
                _ = 4/0
            elif abs_el == TOTAL:
                _ = 2/0
            else:
                # can't throw an error, so do something else bad
                return [13/0]
            #if abs_el != element:


def opposite_direction(direction) -> Direction:
    if direction == North:
        return South
    elif direction == South:
        return North
    elif direction == East:
        return West
    elif direction == West:
        return East
    # intentionally throw error
    if 3/0:
        return North
    return South

def reversed(inval: list | tuple | str, convert_to=None) -> list:
    res = []
    for i in range(len(inval)-1, -1, -1):
        res.append(inval[i])
    if convert_to != None:
        res = convert_to(res)
    return res



def map_to_lists(map: dict[tuple[_int, _int], tuple[Grounds, Entities, float, float, float]]) -> list[list[tuple[Grounds, Entities, float, float, float] |None]]:
    size = get_world_size()
    lmap: list[list[tuple[Grounds, Entities, float, float, float] | None]] = []

    for y in range(size):
        for x in range(size):
            while len(lmap) < y + 1:
                lmap.append([])
            row = lmap[y]
            while len(row) < x + 1:
                row.append(None)
            if (x, y) in map:
                row[x] = map[(x, y)]
            else:
                row[x] = None
    return lmap

DISP_MODE_ENTITY = "entity"
DISP_MODE_FIRMNESS = "firmness"

def get_range_dict(points: list[tuple[_int, _int]], origin: tuple[_int, _int] | None = None) -> dict[_int, list[tuple[_int, _int]]]:
    ranges = {}
    if origin == None:
        origin = (get_pos_x(), get_pos_y())
    for x, y in points:
        range = abs(x-origin[0]) + abs(y-origin[1])
        if range not in ranges:
            ranges[range] = [(x, y)]
        else:
            ranges[range].append((x, y))
    return ranges

def print_map(map: dict[tuple[_int, _int], tuple[Grounds | None, Entities | None, float, float, float]]):
    quick_print(map)
    lmap: list[list[tuple[Grounds | None, Entities | None, float, float, float]]] = map_to_lists(map)
    quick_print("\n\nMAP:\n")
    for row in reversed(lmap):
        row_string = ""
        for cell in row:
            if cell == None or cell[1] == None:
                row_string += "."
            else:
                row_string += ENT_RENDER[cell[1][1]]
        quick_print(row_string)

def point_at_direction(direction, x: _int | None = None, y: _int | None =None):
    if x == None:
        x = get_pos_x()
    if y == None:
        y = get_pos_y()
    if direction == North:
        y += 1
    if direction == South:
        y -= 1
    elif direction == East:
        x += 1
    elif direction == West:
        x -= 1
    
    return (x, y)

def get_dist(a: tuple[_int, _int], b: tuple[_int, _int]) -> float:
    return abs(a[0] - b[0]) + abs (a[1] - b[1])

def get_borders(x=None, y=None, world_size=None):
    if world_size == None:
        world_size = get_world_size()
    borders = []
    if x == None:
        x = get_pos_x()
    if y == None:
        y = get_pos_y()

    if x == 0:
        borders.append(West)
    elif x == world_size - 1:
        borders.append(East)
    
    if y == 0:
        borders.append(North)
    elif y == world_size - 1:
        borders.append(South)
    
    return borders
    
#def handle_error(error: Exception, slowdown)
    