import math

import pygame

def normalize_vector(x: int, y: int) -> pygame.math.Vector2:
		magnitude: float = math.sqrt(x**2 + y**2)

		if magnitude == 0:
			return pygame.math.Vector2(0.0, 0.0)
		else:
			normalized_x: float = x / magnitude
			normalized_y: float = y / magnitude
			return pygame.math.Vector2(normalized_x, normalized_y)