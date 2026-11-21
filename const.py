


from __builtins__ import (
    Any,
    Direction,
    East,
    Entities,
    Entity,
    Item,
    Items,
    North,
    South,
    West,
)

MAX_GRASS = 3
CARROT_MIN = 150

ENT_RENDER = {
    Entities.Carrot: "^",
    Entities.Tree: "T",
    Entities.Bush: "B",
    Entities.Pumpkin: "P",
    Entities.Dead_Pumpkin: "b",
    Entities.Grass: "g",
}
def _items(in_dict: dict) -> list[tuple[Any, Any]]:
    items = []
    for key in in_dict:
        items.append((key, in_dict[key]))
    return items
ITEMS: dict[Item, set[Entity]] = {
    Items.Hay: {Entities.Grass,}, Items.Wood: {Entities.Tree, Entities.Bush},
    Items.Carrot: {Entities.Carrot,}, Items.Pumpkin: {Entities.Pumpkin,},
    Items.Bamboo: {Entities.Bamboo,}}

ENTITIES: dict[Entity, Item] = {}
for item, entities in _items(ITEMS):
    for ent in entities:
        ENTITIES[ent] = item
        
DIRECTIONS: dict[Direction, tuple[int, int]] = {North: (0, 1), East: (1, 0), South: (0, -1), West: (-1, 0)}

