import pygame

class Time_Handler:
    def __init__(self):
        self.m_clock: pygame.time.Clock = pygame.time.Clock()
        self.m_delta_time_ms: int = 0
        self.m_delta_time_s: float = 0
        self.m_total_duration_ms: int = 0

    def tick(self, framerate: float = 0):
        self.m_delta_time_ms = self.m_clock.tick(framerate)
        self.m_delta_time_s = self.m_delta_time_ms / 1000.0
        self.m_total_duration_ms += self.m_delta_time_ms

    def get_delta_time_ms(self) -> int:
        return self.m_delta_time_ms
    
    def get_delta_time_s(self) -> float:
        return self.m_delta_time_s

    def get_fps(self) -> float:
        return self.m_clock.get_fps()

    def get_total_duration_ms(self) -> int:
        return self.m_total_duration_ms

    def reset_total_duration(self) -> None:
        self.m_total_duration_ms = 0