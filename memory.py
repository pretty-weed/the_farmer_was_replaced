from __builtins__ import (
	Direction,
	Entities,
	Grounds,
	get_time,
	quick_print,
)

last_direction: Direction | None = None

NO_MEMORY = "lkaslkdfklasdfkladfskljalskdfalkdfjlkkjljlkasdlkfjdlkfalkdfjkafdlkj"
# Ground type, Entity, stability, hardness, observation time
map: dict[tuple[ int, int], tuple[Grounds | None, Entities | None, float, float, float]] = {}


def set_cell_entity_and_ground(x:int, y:int, entity: Entities=NO_MEMORY, ground: Grounds=NO_MEMORY) -> tuple[Grounds | None, Entities | None, float, float, float]:
	global map
	if (x,y) not in map or map[(x,y)][1] == None:
		
		quick_print("creating new cell at " + str((x,y)))
		cell = ((x,y), (ground, entity, None, None, get_time()))
		
	else:
		cell = map[(x,y)]
		if ground == NO_MEMORY and cell[1] != None:
			ground = cell[1][0]
		if entity == NO_MEMORY and cell[1] != None:
			entity = cell[1][1]
		
		quick_print("Setting cell value")
		cell = (
			(x,y), (ground, entity, cell[1][2], cell[1][3], get_time())
		)
		quick_print("cell is " + str(cell))
	if (x,y) in map:
		quick_print("updating "+ str((x,y)) + " from " + str(map[(x,y)]))
	else:
		quick_print("adding cell at "+ str((x,y)))
	map[(x,y)] = cell
	print("map cell after set: ", map[(x,y)])
	return cell