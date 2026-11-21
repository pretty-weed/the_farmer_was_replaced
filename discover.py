from __builtins__ import (
    Grounds,
    get_entity_type,
    get_ground_type,
    get_pos_x,
    get_pos_y,
    get_pos_z,
)
from const import ENTITIES
from movement import weave


def find_surface_list(
        grounds=None, entities=None, 
        measure_z: bool = False,
        skip:set[tuple[int, int]] | None = None, reset=False) -> dict[Ground | Item, dict[tuple[int, int], int]]:
        
    found = {}
    if (grounds in [None, True] and grounds == entities) or (grounds != None and entities != None):
        if grounds == entities:
            def get_here(g_or_e) -> bool:
                return True
        elif grounds == True:
            def get_here(g_or_e) -> bool:
                return g_or_e in Grounds or g_or_e in entities
        elif entities == True:
            def get_here(g_or_e) -> bool:
                return g_or_e in ENTITIES or g_or_e in grounds
        else:
            # neither true, both not None    
            def get_here(g_or_e) -> bool:
                return g_or_e in grounds or g_or_e in entities          

        def check_cell(x, y):
            
            ground = get_ground_type()
            if get_here(ground):
                if ground not in found:
                    found[ground] = {}
                found[ground][(x, y)] = get_pos_z()
            ent = get_entity_type()
            if get_here(ent):
                if ent not in found:
                    found[ent] = {}
                found[ent][(x, y)] = get_pos_z()
    elif grounds != None:
        def check_cell(x, y):
            ground = get_ground_type()
            if grounds == True or ground in grounds:
                if ground not in found:
                    found[ground] = {}
                found[ground][(x, y)] = get_pos_z()
    elif entities != None:
        def check_cell(x, y):
            ent = get_entity_type()
            if entities == True or ent in entities:
                if ent not in found:
                    found[ent] = {}
                found[ent][(x, y)] = get_pos_z()
    # there's no else as I can't raise an exception
        

    conditions = []
    if skip:
        def skip_eh() -> bool:
            return (get_pos_x(), get_pos_y()) not in skip
        conditions.append(skip_eh)
    weave([(1.0, conditions, check_cell)], reset)
    return found
    