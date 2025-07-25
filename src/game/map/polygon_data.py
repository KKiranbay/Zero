from typing import List, Tuple

import pygame
class PolygonData:
	"""Data structure holding polygon vertices and associated colors."""

	def __init__(self, vertices: List[pygame.Vector2],
	             fill_color: Tuple[int, int, int] = (100, 100, 100),
	             outline_color: Tuple[int, int, int] = (255, 255, 255),
	             outline_width: int = 2) -> None:
		self.m_vertices: List[pygame.Vector2] = vertices.copy()
		self.m_fill_color: Tuple[int, int, int] = fill_color
		self.m_outline_color: Tuple[int, int, int] = outline_color
		self.m_outline_width: int = outline_width

		self.m_middle_point: pygame.Vector2 = self._calculate_middle_point()
		self.m_circumference: float = self._calculate_circumference()

	def _calculate_middle_point(self) -> pygame.Vector2:
		"""Calculate the middle point of the polygon based on its vertices."""
		if not self.m_vertices:
			return pygame.Vector2(0, 0)

		x_sum = sum(vertex.x for vertex in self.m_vertices)
		y_sum = sum(vertex.y for vertex in self.m_vertices)
		num_vertices = len(self.m_vertices)

		return pygame.Vector2(x_sum // num_vertices, y_sum // num_vertices)

	def _calculate_circumference(self) -> float:
		"""Calculate the circumference of the polygon."""
		if len(self.m_vertices) < 2:
			return 0.0

		circumference = 0.0
		for i in range(len(self.m_vertices)):
			x1, y1 = self.m_vertices[i].x, self.m_vertices[i].y
			x2, y2 = self.m_vertices[(i + 1) % len(self.m_vertices)].x, self.m_vertices[(i + 1) % len(self.m_vertices)].y
			circumference += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

		return circumference

	def get_middle_point(self) -> pygame.Vector2:
		"""Get the middle point of the polygon."""
		return self.m_middle_point

	def get_vertices(self) -> List[pygame.Vector2]:
		"""Get a copy of the polygon vertices."""
		return self.m_vertices.copy()

	def set_vertices(self, vertices: List[pygame.Vector2]) -> None:
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

	def select_a_point_randomly_on_vertices(self) -> pygame.Vector2:
		"""Select a point on the polygon vertices, edges, or in between the consequent edges."""
		if not self.m_vertices:
			return pygame.Vector2(0, 0)

		"""Select a value between 0 and the circumference of the polygon."""
		import random
		random_point_distance_from_start = random.uniform(0, self.m_circumference)

		"""Select a point on the polygon based on the random distance."""
		current_distance = 0.0
		for i in range(len(self.m_vertices)):
			x1, y1 = self.m_vertices[i].x, self.m_vertices[i].y
			x2, y2 = self.m_vertices[(i + 1) % len(self.m_vertices)].x, self.m_vertices[(i + 1) % len(self.m_vertices)].y
			edge_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

			if current_distance + edge_length >= random_point_distance_from_start:
				# Calculate the exact point on the edge
				t = (random_point_distance_from_start - current_distance) / edge_length
				return pygame.Vector2(int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))

			current_distance += edge_length

		return self.m_vertices[-1]

	def check_if_given_rect_collides_with_polygon_s_vertices(self, rect: pygame.Rect) -> bool:
		"""Check if a rectangle collides with the polygon's vertices."""
		for vertex in self.m_vertices:
			vertex_rect = pygame.Rect(vertex.x, vertex.y, 1, 1)
			if rect.colliderect(vertex_rect):
				return True
		return False

	def point_in_polygon(self, point: pygame.Vector2) -> bool:
		"""Check if a point is inside a polygon using ray casting algorithm.

		Args:
			point: (x, y) coordinate tuple to test

		Returns:
			True if point is inside polygon, False otherwise
		"""

		if len(self.m_vertices) < 3:
			return False

		num_vertices: int = len(self.m_vertices)
		inside: bool = False

		first_Vector2 = self.m_vertices[0]
		for i in range(1, num_vertices + 1):
			second_Vector2 = self.m_vertices[i % num_vertices]

			if point.y > min(first_Vector2.y, second_Vector2.y) and point.y <= max(first_Vector2.y, second_Vector2.y) and point.x <= max(first_Vector2.x, second_Vector2.x):
				if first_Vector2.y != second_Vector2.y:
					xinters = (point.y - first_Vector2.y) * (second_Vector2.x - first_Vector2.x) / (second_Vector2.y - first_Vector2.y) + first_Vector2.x

				if first_Vector2.x == second_Vector2.x or point.x <= xinters:
					inside = not inside

			first_Vector2 = second_Vector2

		return inside