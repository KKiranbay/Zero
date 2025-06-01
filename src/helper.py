import math

import pygame

def normalize_vector(vector: pygame.math.Vector2) -> pygame.math.Vector2:
		magnitude: float = math.sqrt(vector.x**2 + vector.y**2)

		if magnitude == 0:
			return pygame.math.Vector2(0.0, 0.0)
		else:
			normalized_x: float = vector.x / magnitude
			normalized_y: float = vector.y / magnitude
			return pygame.math.Vector2(normalized_x, normalized_y)