# MapRenderer class for rendering map polygons to pygame surfaces
# Key features:
# - Renders main polygon and interior polygons with their respective colors
# - Supports filled polygons and outlined polygons

from typing import Tuple, Optional
import pygame
from game.map.map import Map, PolygonData

class MapRenderer:
	def __init__(self) -> None:
		# Rendering options
		self.m_render_filled: bool = True
		self.m_render_outlines: bool = True

	def set_render_options(self, render_filled: bool = True, render_outlines: bool = True) -> None:
		"""Set rendering options for polygons.

		Args:
			render_filled: Whether to render filled polygons
			render_outlines: Whether to render polygon outlines
		"""
		self.m_render_filled = render_filled
		self.m_render_outlines = render_outlines

	def render_map(self, surface: pygame.Surface, game_map: Map | None) -> None:
		"""Render the entire map to the given surface.

		Args:
			surface: Pygame surface to render on
			game_map: Map object to render
		"""
		if game_map is None:
			return

		# Render main polygon
		self._render_polygon(surface, game_map.get_main_polygon())

		# Render interior polygons
		for interior_polygon in game_map.get_interior_polygons():
			self._render_polygon(surface, interior_polygon)

	def render_main_polygon_only(self, surface: pygame.Surface, game_map: Map) -> None:
		"""Render only the main polygon.

		Args:
			surface: Pygame surface to render on
			game_map: Map object containing the main polygon
		"""
		self._render_polygon(surface, game_map.get_main_polygon())

	def render_interior_polygons_only(self, surface: pygame.Surface, game_map: Map) -> None:
		"""Render only the interior polygons.

		Args:
			surface: Pygame surface to render on
			game_map: Map object containing interior polygons
		"""
		for interior_polygon in game_map.get_interior_polygons():
			self._render_polygon(surface, interior_polygon)

	def _render_polygon(self, surface: pygame.Surface, polygon_data: PolygonData) -> None:
		"""Render a single polygon with its colors.

		Args:
			surface: Pygame surface to render on
			polygon_data: PolygonData object containing vertices and colors
		"""
		vertices = polygon_data.get_vertices()

		if len(vertices) < 3:
			return

		# Render filled polygon
		if self.m_render_filled:
			pygame.draw.polygon(surface, polygon_data.get_fill_color(), vertices)

		# Render polygon outline
		if self.m_render_outlines and polygon_data.get_outline_width() > 0:
			pygame.draw.polygon(surface, polygon_data.get_outline_color(),
			                  vertices, polygon_data.get_outline_width())

	def render_polygon_wireframe(self, surface: pygame.Surface, polygon_data: PolygonData,
	                           color: Optional[Tuple[int, int, int]] = None,
	                           width: Optional[int] = None) -> None:
		"""Render a polygon as wireframe with custom color and width.

		Args:
			surface: Pygame surface to render on
			polygon_data: PolygonData object to render
			color: Override color for wireframe (uses polygon's outline color if None)
			width: Override width for wireframe (uses polygon's outline width if None)
		"""
		vertices = polygon_data.get_vertices()

		if len(vertices) < 3:
			return

		render_color = color if color is not None else polygon_data.get_outline_color()
		render_width = width if width is not None else polygon_data.get_outline_width()

		if render_width > 0:
			pygame.draw.polygon(surface, render_color, vertices, render_width)

	def render_polygon_filled(self, surface: pygame.Surface, polygon_data: PolygonData,
	                        color: Optional[Tuple[int, int, int]] = None) -> None:
		"""Render a polygon filled with custom color.

		Args:
			surface: Pygame surface to render on
			polygon_data: PolygonData object to render
			color: Override color for fill (uses polygon's fill color if None)
		"""
		vertices = polygon_data.get_vertices()

		if len(vertices) < 3:
			return

		render_color = color if color is not None else polygon_data.get_fill_color()
		pygame.draw.polygon(surface, render_color, vertices)
