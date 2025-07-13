from typing import List, Tuple

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