import pygame

import colors

class Character:
    def __init__(self, char_size: int, char_speed: float, screen_width: int, screen_height: int):
        self.m_char_size: int = char_size
        self.m_char_x: float = screen_width // 2 - self.m_char_size // 2
        self.m_char_y: float = screen_height // 2 - self.m_char_size // 2
        self.m_char_speed: float = char_speed
        self.m_char_screen_x: float = 0
        self.m_char_screen_y: float = 0

    def move_char(self, keys):
        if keys[pygame.K_a]:
            self.m_char_x -= self.m_char_speed
        if keys[pygame.K_d]:
            self.m_char_x += self.m_char_speed
        if keys[pygame.K_w]:
            self.m_char_y  -= self.m_char_speed
        if keys[pygame.K_s]:
            self.m_char_y  += self.m_char_speed

    def draw_char(self, screen: pygame.Surface, cam_pos_x: float, cam_pos_y: float):
        self.m_char_screen_x = self.m_char_x - cam_pos_x
        self.m_char_screen_y = self.m_char_y - cam_pos_y
        pygame.draw.rect(screen, colors.RED, (self.m_char_screen_x, self.m_char_screen_y, self.m_char_size, self.m_char_size))
