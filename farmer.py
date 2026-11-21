

from __builtins__ import (
    Entities,
    Entity,
    Item,
    can_harvest,
    get_companion,
    get_entity_type,
    get_world_size,
    harvest,
    random,
)
from const import ENTITIES, ITEMS
from movement import go_to, weave
from stdlib_patch import items, sum
from tasks import do_plant
from util import ent_to_item_count, find_areas, random_choice, resolve_entities


def prioritize(goals: list[Item | Entity] | set[Item | Entity], key=ent_to_item_count, invert_key=True) -> dict[int, list[Entity]]:

    ent_goals = {}
    if invert_key:
        base_key = key
        all_keys = []
        for goal in goals:
            all_keys.append(key(random_choice(resolve_entities(goal))))
        key_sum = sum(all_keys)
        def key(ent):
            print('in key for ' + str(ent))
            return key_sum - base_key(ent)
    
    for target in goals:
        quick_print('target: ' + str(target))
        quick_print('in entities: ' + str(target in ENTITIES) + '; in items: ' + str(target in ITEMS) + '; item in entities: ' + str(ITEMS[target]))
        if target in ENTITIES:
            entity = target
        else:
            entity = random_choice(ITEMS[target])
        weight = key(entity)
        if weight not in ent_goals:
            ent_goals[weight] = []
        ent_goals[weight].append(entity)
        
    return ent_goals

def make_simple_planter(entity: Entity, harvest_loops: int = 3):
    def ent_planter(x, y):
        return _simple_planter(x, y, entity, harvest_loops)
    return ent_planter

def _simple_planter(x: int, y: int, entity: Entity, harvest_check_loops=3, ):
    harvest_loops = 0
    plantable = get_entity_type() == None
    while harvest_loops < harvest_check_loops and not plantable:
        if can_harvest():
            harvest()
            plantable = True
        harvest_loops += 1
    if not plantable:
        return False
    do_plant(entity)
    return True

def make_buddy_planter(entity: Entity, harvest_loops: int = 3, buddy_chance=0.1):
    def _this_buddy_planter(x: int, y: int) -> bool:
        return _buddy_planter(x, y, entity, buddy_chance, harvest_loops)
    return _this_buddy_planter

def _buddy_planter(x: int, y: int, entity: Entity, chance=0.1, harvest_loops=3) -> bool:
    _simple_planter(x, y, entity, harvest_loops)
    if random() < chance:
        buddy_ent, buddy_pos = get_companion()
        go_to(buddy_pos)
        if not get_entity_type():
            do_plant(buddy_ent)
        go_to((x,y))
    return False




BASIC_PLANTERS = {}
for ent in Entities:
    BASIC_PLANTERS[ent] = make_simple_planter(ent)

BUDDY_PLANTERS = {}
for ent in Entities:
    BUDDY_PLANTERS[ent] = make_buddy_planter(ent)

def _second_item_key(val): 
    return val[1]

def farm_foreman(desired_items: set[Item], prioritizer=prioritize):
    quick_print("desired items")
    quick_print(desired_items)
    goals: dict[int, list[Entity]] = prioritizer(desired_items)
    quick_print("goals")
    quick_print(goals)
    goal_ents: list[Entity] = []
    goal_weights = []
    total_weight = 0
    for count, ents in items(goals):
        total_weight += count * len(ents)
    quick_print("items: " + str(items(goals)))
    for count, ents in items(goals):
        quick_print('weight: ' + str(count) + ', ents: ' + str(ents))
        for ent in ents:
            goal_ents.append(ent)
            goal_weights.append(count/total_weight)
    ws = get_world_size()
    quick_print("b4 find areas")
    quick_print("goal_weights: " + str(goal_weights))

    ent_areas = find_areas(goal_weights, (ws, ws))
    for a_bl, a_tr, ent_idx in ent_areas:
        planterizer((a_bl, a_tr), goal_ents[ent_idx])

def planterizer(area: tuple[tuple[int, int], tuple[int, int]], entity: Entity, companion_chance=0.1):
    if companion_chance:
        weave([(1.0, [], make_buddy_planter(entity, 3, companion_chance))])
    else:
        weave([(1.0, [], make_simple_planter(entity))])

def farmerator(goals: dict[Entity, int], clear:bool=False, companion_threshold=2.0):
    priorities: dict[Entity, int] = dict(goals)
    next_weight = max(priorities)
    
    while priorities:
        weight = next_weight
        priority = priorities.pop(weight)
        if priorities:
            next_weight = max(priorities)
            next_entities = priorities[next_weight]
            possible_entities = resolve_entities(priority)
            # ToDo figure out how to prioritize
            continue

if __name__ == "__main__":
    farm_foreman(set([Items.Bamboo, Items.Pumpkin]))



