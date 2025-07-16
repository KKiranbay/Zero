# Map class representing the game area with polygon boundaries
# Key features:
# - Stores a mandatory main polygon boundary with optional interior polygons
# - Main polygon contains all other polygons and defines the playable area
# - Interior polygons are obstacles/walls within the main boundary

import pygame

from typing import Tuple
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

	def point_in_main_polygon(self, point: pygame.Vector2) -> bool:
		"""Check if a point is inside the main polygon boundary.

		Args:
			point: (x, y) coordinate tuple

		Returns:
			True if point is inside main polygon, False otherwise
		"""
		return self.m_main_polygon.point_in_polygon(point)

	def point_in_interior_polygons(self, point: pygame.Vector2) -> bool:
		"""Check if a point is inside any interior polygon.

		Args:
			point: (x, y) coordinate tuple

		Returns:
			True if point is inside any interior polygon, False otherwise
		"""
		for interior_polygon in self.m_interior_polygons:
			if interior_polygon.point_in_polygon(point):
				return True
		return False

	def point_in_playable_area(self, point: pygame.Vector2) -> bool:
		"""Check if a point is in playable area (main polygon but not in interior polygons).

		Args:
			point: (x, y) coordinate tuple

		Returns:
			True if point is in playable area, False otherwise
		"""
		return (self.point_in_main_polygon(point) and not self.point_in_interior_polygons(point))
