from enum import Enum

import pygame

import colors

class NPC_Type(Enum):
    ENEMY = 1
    FRIENDLY = 2

class NPC:
    def __init__(self, npc_type: NPC_Type, npc_pos_x: float, npc_pos_y: float, npc_size: float):
        self.m_type: NPC_Type = npc_type
        self.m_pos_x: float = npc_pos_x
        self.m_pos_y: float = npc_pos_y
        self.m_npc_size: float = npc_size
        self.m_npc_half_size: float = npc_size

        self.m_rect = pygame.Rect(self.m_pos_x - self.m_npc_half_size, self.m_pos_y - self.m_npc_half_size, npc_size, npc_size)

    def draw_npc(self, ground: pygame.Surface):
        pygame.draw.rect(ground, colors.PURPLE, self.m_rect)