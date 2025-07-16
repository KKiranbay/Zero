# Collision types enum for game objects
# Key features:
# - Defines different collision result types
# - Used by game objects to determine collision behavior

from enum import Enum

class CollisionType(Enum):
    NO_COLLISION = "no_collision"
    WALL_COLLISION = "wall_collision"