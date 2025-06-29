# NPC Factory Module
# This module provides factory functions for creating NPC instances.
# Key functions:
# - create_npc: Creates NPC instances with specified parameters
# - NPC_Type: Exports NPC type enumeration

from typing import TYPE_CHECKING
import pygame

from game.game_objects.npcs.npc import NPC, NPC_Type

if TYPE_CHECKING:
	from game.game import Game

def create_npc(game: 'Game', npc_type: NPC_Type, pos: pygame.Vector2, size: pygame.Vector2) -> NPC:
	return NPC(game, npc_type, pos, size)

# Export NPC_Type for convenience
__all__ = ['create_npc', 'NPC_Type']
