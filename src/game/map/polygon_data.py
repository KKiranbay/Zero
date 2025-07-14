from typing import List, Tuple

import pygame
class PolygonData:
	"""Data structure holding polygon vertices and associated colors."""

	def __init__(self, vertices: List[Tuple[int, int]],
	             fill_color: Tuple[int, int, int] = (100, 100, 100),
	             outline_color: Tuple[int, int, int] = (255, 255, 255),
	             outline_width: int = 2) -> None:
		self.m_vertices: List[Tuple[int, int]] = vertices.copy()
		self.m_fill_color: Tuple[int, int, int] = fill_color
		self.m_outline_color: Tuple[int, int, int] = outline_color
		self.m_outline_width: int = outline_width

		self.m_middle_point: Tuple[int, int] = self._calculate_middle_point()
		self.m_circumference: float = self._calculate_circumference()

	def _calculate_middle_point(self) -> Tuple[int, int]:
		"""Calculate the middle point of the polygon based on its vertices."""
		if not self.m_vertices:
			return (0, 0)

		x_sum = sum(x for x, y in self.m_vertices)
		y_sum = sum(y for x, y in self.m_vertices)
		num_vertices = len(self.m_vertices)

		return (x_sum // num_vertices, y_sum // num_vertices)

	def _calculate_circumference(self) -> float:
		"""Calculate the circumference of the polygon."""
		if len(self.m_vertices) < 2:
			return 0.0

		circumference = 0.0
		for i in range(len(self.m_vertices)):
			x1, y1 = self.m_vertices[i]
			x2, y2 = self.m_vertices[(i + 1) % len(self.m_vertices)]
			circumference += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

		return circumference

	def get_middle_point(self) -> Tuple[int, int]:
		"""Get the middle point of the polygon."""
		return self.m_middle_point

	def get_vertices(self) -> List[Tuple[int, int]]:
		"""Get a copy of the polygon vertices."""
		return self.m_vertices.copy()

	def set_vertices(self, vertices: List[Tuple[int, int]]) -> None:
		"""Set new vertices for the polygon."""
		if len(vertices) >= 3:
			self.m_vertices = vertices.copy()

	def get_fill_color(self) -> Tuple[int, int, int]:
		"""Get the fill color of the polygon."""
		return self.m_fill_color

	def set_fill_color(self, color: Tuple[int, int, int]) -> None:
		"""Set the fill color of the polygon."""
		self.m_fill_color = color

	def get_outline_color(self) -> Tuple[int, int, int]:
		"""Get the outline color of the polygon."""
		return self.m_outline_color

	def set_outline_color(self, color: Tuple[int, int, int]) -> None:
		"""Set the outline color of the polygon."""
		self.m_outline_color = color

	def get_outline_width(self) -> int:
		"""Get the outline width of the polygon."""
		return self.m_outline_width

	def set_outline_width(self, width: int) -> None:
		"""Set the outline width of the polygon."""
		self.m_outline_width = max(0, width)

	def select_a_point_randomly_on_vertices(self) -> Tuple[int, int]:
		"""Select a point on the polygon vertices, edges, or in between the consequent edges."""
		if not self.m_vertices:
			return (0, 0)

		"""Select a value between 0 and the circumference of the polygon."""
		import random
		random_point_distance_from_start = random.uniform(0, self.m_circumference)

		"""Select a point on the polygon based on the random distance."""
		current_distance = 0.0
		for i in range(len(self.m_vertices)):
			x1, y1 = self.m_vertices[i]
			x2, y2 = self.m_vertices[(i + 1) % len(self.m_vertices)]
			edge_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

			if current_distance + edge_length >= random_point_distance_from_start:
				# Calculate the exact point on the edge
				t = (random_point_distance_from_start - current_distance) / edge_length
				return (int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))

			current_distance += edge_length

		return self.m_vertices[-1]

	def check_if_given_rect_collides_with_polygon_s_vertices(self, rect: pygame.Rect) -> bool:
		"""Check if a rectangle collides with the polygon's vertices."""
		for vertex in self.m_vertices:
			vertex_rect = pygame.Rect(vertex[0], vertex[1], 1, 1)
			if rect.colliderect(vertex_rect):
				return True
		return False

