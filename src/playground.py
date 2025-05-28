import pygame

class Playground:
    def __init__(self, width, height):
        self.m_width = width
        self.m_height = height
        self.m_rect = pygame.Rect(0, 0, width, height)
        
    def draw_playground(self, screen, color, camera_x, camera_y):
        pygame.draw.rect(screen, color, (self.m_rect.x - camera_x, self.m_rect.y - camera_y, self.m_width, self.m_height))