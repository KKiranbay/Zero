import pygame

class Screen:
    def __init__(self, screen_width: int, screen_height: int, caption: str):
        self.m_screen_width: int = screen_width
        self.m_screen_height: int = screen_height
        self.m_surface: pygame.Surface = pygame.display.set_mode((self.m_screen_width, self.m_screen_height))
        pygame.display.set_caption(caption)
