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
	move,
)


# period (do 1 / every n), conditions, callable
def weave(tasks:list[tuple[float, list[Callable[[],bool]], Callable[[int, int], Any]]]):
	world_size: WorldSizes = get_world_size()
	while get_pos_x():
		move(East)
	while get_pos_y():
		move(South)
	travel: None | Direction = None
	counter = 0
	for x in range(world_size): 
		for y in range(world_size):
			px = get_pos_x()
			py = get_pos_y()
			travel = None

			if (py == world_size - 1 and (not px % 2)) or (py == 0 and (px % 2)) :
				if py == world_size -1:
					if world_size % 2:
						for _ in range(world_size-1):
							move(South)
					for _ in range(world_size-1):
						move(West)
					continue
				
				else:
					travel = East
			else:
				if px % 2:
					travel = South
				else:
					travel = North
			for period, conditions, task_do in tasks:
				if not counter % period:
					for condition in conditions:
						if not condition():
							continue
					task_do(px, py)
			move(travel)

			counter += 1





