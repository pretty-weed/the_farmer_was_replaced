
from __builtins__ import Items, get_ground_type, num_items, random
from util import get_borders

COND_NE = "!="
COND_EQ = "="
COND_GT = ">"
COND_GTE = ">="
COND_LT = "<"
COND_LTE = "<="
def _cond_ne(a, b) -> bool:
	return a != b

def _cond_eq(a, b) -> bool:
	return a == b
def _cond_gt(a, b) -> bool:
	return a > b
def _cond_gte(a,b) -> bool:
	return a >= b

def _cond_lt(a,b) -> bool:
	return a < b

def _cond_lte(a,b) -> bool:
	return a <= b

ABOVE = 1
EQUAL = 0
BELOW = -1

CONDITIONS = {
	COND_NE: _cond_ne,
	COND_EQ: _cond_eq,
	COND_GT: _cond_gt,
	COND_LT: _cond_lt,
	COND_GTE: _cond_gte,
	COND_LTE: _cond_lte
}

def rand(threshold: float = 0.5) -> bool:
	return random() < threshold

def resource_ratio(a: Items, b: Items, threshold: float, condition: int=ABOVE):
	rat = num_items(a) / num_items(b)
	if condition > 0:
		return rat > threshold
	elif condition == 0:
		return rat == threshold
	else:
		return rat < threshold

def get_resource_ratio_cond(a: Items, b: Items, threshold: float, condition: int = ABOVE):
	def new_cond(a, b, threshold, condition) -> bool:
		return resource_ratio(a, b, threshold, condition)

	return new_cond

def get_rand_cond(threshold: float=0.5):
	def new_cond(threshold) -> bool:
		return rand(threshold)

def get_ground_type_cond(types: list[Ground], direction: Direction | None = None):
	
	def new_ground_type_cond():
		return get_ground_type(direction) in types

	return new_ground_type_cond

def is_on_border(x: int | None = None, y: int | None = None, world_size: int | None = None) -> bool:
	return get_borders(x, y, world_size) != []

def not_on_border(x: int | None = None, y: int | None = None, world_size: int | None = None) -> bool:
	return get_borders(x, y, world_size) == []