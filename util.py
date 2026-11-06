

from __builtins__ import (
	Direction,
	East,
	Entities,
	Entity,
	Grounds,
	Item,
	North,
	South,
	West,
	get_pos_x,
	get_pos_y,
	get_world_size,
	quick_print,
)
from const import ENT_RENDER, ENTITIES, ITEMS


def update(da: dict, db: dict) -> None:
	for key in db:
		da[key] = db[key]

def item_to_entities(item: Item) -> set[Entity]:
	return ITEMS[item]

def entity_to_item(entity: Entity) -> Item:
	return ENTITIES[entity]

def resolve_x(x) -> int:
	if x == None:
		return get_pos_x()
	return x

def resolve_y(y) -> int:
	if y == None:
		return get_pos_y()
	return y

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



def map_to_lists(map: dict[tuple[int, int], tuple[Grounds, Entities, float, float, float]]) -> list[list[tuple[Grounds, Entities, float, float, float] |None]]:
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

def print_map(map: dict[tuple[int, int], tuple[Grounds | None, Entities | None, float, float, float]]):
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

def point_at_direction(direction, x: int | None = None, y: int | None =None):
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

def get_dist(a: tuple[int, int], b: tuple[int, int]) -> float:
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
	