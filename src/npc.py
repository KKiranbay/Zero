from enum import Enum

import pygame

import colors

class NPC_Type(Enum):
    ENEMY = 1
    FRIENDLY = 2

class NPC:
    def __init__(self, npc_type: NPC_Type, npc_pos_x: float, npc_pos_y: float, npc_size: float):
        self.m_type: NPC_Type = npc_type
        self.m_npc_pos_x: float = npc_pos_x
        self.m_npc_pos_y: float = npc_pos_y
        self.m_npc_size: float = npc_size

    def draw_npc(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        pygame.draw.circle(screen, colors.BLUE, (self.m_npc_pos_x - camera_x, self.m_npc_pos_y - camera_y), self.m_npc_size)