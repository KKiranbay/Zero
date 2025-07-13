# Map class representing the game area with polygon boundaries
# Key features:
# - Stores a mandatory main polygon boundary with optional interior polygons
# - Main polygon contains all other polygons and defines the playable area
# - Interior polygons are obstacles/walls within the main boundary

from typing import List, Tuple
from game.map.polygon_data import PolygonData

class Map:
	def __init__(self, main_polygon_data: PolygonData) -> None:
		# Mandatory main polygon that defines the overall playable area
		if len(main_polygon_data.m_vertices) < 3:
			raise ValueError("Main polygon must have at least 3 vertices")

		self.m_main_polygon: PolygonData = main_polygon_data

		# Set of interior polygons (obstacles/walls within the main boundary)
		self.m_interior_polygons: set[PolygonData] = set()

	def get_main_polygon(self) -> PolygonData:
		"""Get the main polygon data."""
		return self.m_main_polygon

	def set_main_polygon(self, polygonData: PolygonData) -> None:
		"""Set new main polygon with colors."""
		if len(polygonData.m_vertices) < 3:
			raise ValueError("Main polygon must have at least 3 vertices")

		self.m_main_polygon = polygonData

	def add_interior_polygon(self, polygon_data: PolygonData) -> PolygonData:
		"""Add an interior polygon (obstacle/wall) to the map.

		Args:
			vertices: List of (x, y) coordinate tuples defining the polygon vertices
			fill_color: RGB color for polygon fill
			outline_color: RGB color for polygon outline
			outline_width: Width of the polygon outline

		Returns:
			The created PolygonData object
		"""
		if len(polygon_data.m_vertices) >= 3:
			polygon_data = polygon_data
			self.m_interior_polygons.add(polygon_data)
			return polygon_data
		else:
			raise ValueError("Interior polygon must have at least 3 vertices")

	def remove_interior_polygon(self, polygon_data: PolygonData) -> bool:
		"""Remove an interior polygon from the map.

		Args:
			polygon_data: The PolygonData object to remove

		Returns:
			True if polygon was removed, False if not found
		"""
		if polygon_data in self.m_interior_polygons:
			self.m_interior_polygons.remove(polygon_data)
			return True
		return False

	def get_interior_polygons(self) -> set[PolygonData]:
		"""Get a copy of all interior polygons."""
		return self.m_interior_polygons.copy()

	def clear_interior_polygons(self) -> None:
		"""Remove all interior polygons."""
		self.m_interior_polygons.clear()

	def point_in_main_polygon(self, point: Tuple[int, int]) -> bool:
		"""Check if a point is inside the main polygon.

		Args:
			point: (x, y) coordinate to check

		Returns:
			True if point is inside the main polygon
		"""
		x, y = point
		return self._point_in_polygon(x, y, self.m_main_polygon.get_vertices())

	def point_in_interior_polygons(self, point: Tuple[int, int]) -> bool:
		"""Check if a point is inside any interior polygon.

		Args:
			point: (x, y) coordinate to check

		Returns:
			True if point is inside any interior polygon
		"""
		x, y = point

		for polygon_data in self.m_interior_polygons:
			if self._point_in_polygon(x, y, polygon_data.get_vertices()):
				return True
		return False

	def point_in_playable_area(self, point: Tuple[int, int]) -> bool:
		"""Check if a point is in the playable area (inside main polygon but not in any interior polygon).

		Args:
			point: (x, y) coordinate to check

		Returns:
			True if point is in playable area
		"""
		return (self.point_in_main_polygon(point) and
		        not self.point_in_interior_polygons(point))

	def _point_in_polygon(self, x: int, y: int, polygon: List[Tuple[int, int]]) -> bool:
		"""Ray casting algorithm to check if point is inside polygon."""
		n = len(polygon)
		inside = False

		p1x, p1y = polygon[0]
		for i in range(1, n + 1):
			p2x, p2y = polygon[i % n]
			if y > min(p1y, p2y):
				if y <= max(p1y, p2y):
					if x <= max(p1x, p2x):
						if p1y != p2y:
							xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
							if p1x == p2x or x <= xinters:
								inside = not inside
						elif p1x == p2x:
							inside = not inside
			p1x, p1y = p2x, p2y

		return inside
