from enum import Enum

import pygame

import colors

from playground_object import Playground_Object

class NPC_Type(Enum):
	ENEMY = 1
	FRIENDLY = 2

class NPC(Playground_Object):
	def __init__(self, npc_type: NPC_Type, npc_pos_x: float, npc_pos_y: float, npc_size: float):
		super().__init__(npc_pos_x, npc_pos_y, npc_size)
		self.m_type: NPC_Type = npc_type
		self.image.fill(colors.PURPLE)
