from enum import Enum

enum_val: int = 1
def generateStateId():
	global enum_val
	enum_val += 1
	return enum_val
class StatesEnum(Enum):
	MAIN_MENU		=	generateStateId()
	LOAD_GAME_STATE	=	generateStateId()
	GAME_STATE		=	generateStateId()
	GAME_OVER		=	generateStateId()