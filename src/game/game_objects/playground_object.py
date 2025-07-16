import pygame

import resources.colors as colors

from game.game import Game
from time_handler import Time_Handler

from game.collisions.collision_types import CollisionType
from game.map.map import Map

class PlaygroundObject(pygame.sprite.Sprite):
	def __init__(self, game: Game, pos: pygame.Vector2, size: pygame.Vector2) -> None:
		super().__init__()

		self.m_game: Game = game

		self.m_time_handler: Time_Handler = Time_Handler()

		self.image: pygame.Surface = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
		self.image.fill(colors.WHITE)

		self.m_size: pygame.Vector2 = pygame.Vector2(size)
		self.m_half_size: pygame.Vector2 = self.m_size / 2

		self.m_pos = pygame.math.Vector2(pos)
		self.rect: pygame.Rect = self.image.get_rect()
		self.rect.centerx = round(pos.x)
		self.rect.centery = round(pos.y)

		self.m_reference_vector: pygame.Vector2 = pygame.Vector2(0, -1) # up
		self.m_look_direction: pygame.math.Vector2 = pygame.math.Vector2(0, -1)
		self.m_look_angle: float = self.m_reference_vector.angle_to(self.m_look_direction)

		self.m_attach_anchor_pos: pygame.math.Vector2 = self.m_pos

	def update(self):
		pass

	def update_center_depending_on_pos(self):
		self.rect.centerx = round(self.m_pos.x)
		self.rect.centery = round(self.m_pos.y)

	def setCenter(self, center: pygame.math.Vector2):
		self.rect.centerx = round(center.x)
		self.rect.centery = round(center.y)

	def setPos(self, x: float, y: float):
		self.m_pos.update(x, y)
		self.update_center_depending_on_pos()

	def setDisplacement(self, displacement: pygame.math.Vector2):
		# Check for collisions
		collision_type: CollisionType = check_collisions(self)

		# If collision detected, handle it
		if collision_type != CollisionType.NO_COLLISION:
			handle_collision(self, displacement)
		else:
			self.m_pos += displacement
			self.update_center_depending_on_pos()

		return collision_type

	def check_and_clamp_ip_with_rect(self, rect: pygame.Rect) :
		top_check: bool = rect.top > self.m_pos.y - self.m_half_size.y
		bottom_check: bool = rect.bottom < self.m_pos.y + self.m_half_size.y
		left_check: bool = rect.left > self.m_pos.x - self.m_half_size.x
		right_check: bool = rect.right < self.m_pos.x + self.m_half_size.x

		if (top_check):
			self.m_pos.y = rect.top + self.m_half_size.y

		if (bottom_check):
			self.m_pos.y = rect.bottom - self.m_half_size.y

		if (left_check):
			self.m_pos.x = rect.left + self.m_half_size.x

		if (right_check):
			self.m_pos.x = rect.right - self.m_half_size.x

		if (top_check or bottom_check or left_check or right_check):
			self.update_center_depending_on_pos()

	def check_fully_left_rect(self, rect: pygame.Rect) -> bool :
		top_check: bool = rect.top > self.m_pos.y + self.m_half_size.y
		bottom_check: bool = rect.bottom < self.m_pos.y - self.m_half_size.y
		left_check: bool = rect.left > self.m_pos.x + self.m_half_size.x
		right_check: bool = rect.right < self.m_pos.x - self.m_half_size.x
		return top_check or bottom_check or left_check or right_check

	def get_attach_anchor_pos(self) -> pygame.math.Vector2:
		return self.m_attach_anchor_pos

def check_collisions(playground_object: PlaygroundObject) -> CollisionType:
	"""Check for collisions with map polygons and playground boundaries.

	Returns:
		CollisionType indicating what type of collision occurred
	"""

	game_map: Map | None = playground_object.m_game.get_map()
	if game_map is None:
		return CollisionType.NO_COLLISION

	# Get the four corners of the object's rect
	object_corners = [
		pygame.Vector2(playground_object.rect.topleft),
		pygame.Vector2(playground_object.rect.topright),
		pygame.Vector2(playground_object.rect.bottomleft),
		pygame.Vector2(playground_object.rect.bottomright)
	]

	# Check if object is outside main polygon (playground boundary)
	for corner in object_corners:
		if not game_map.point_in_main_polygon(corner):
			return CollisionType.WALL_COLLISION

	# Check if object intersects with interior polygons (walls/obstacles)
	for corner in object_corners:
		if game_map.point_in_interior_polygons(corner):
			return CollisionType.WALL_COLLISION

	return CollisionType.NO_COLLISION

def handle_collision(playground_object: PlaygroundObject, displacement: pygame.math.Vector2) -> None:
	"""Handle collision by moving object to collision point.

	Args:
		displacement: The displacement vector that caused collision
	"""

	# Binary search to find collision point
	collision_point: pygame.math.Vector2 = _find_collision_point(playground_object, displacement)

	# Set position to collision point
	playground_object.m_pos = collision_point
	playground_object.update_center_depending_on_pos()

def _find_collision_point(playground_object: PlaygroundObject, displacement: pygame.math.Vector2) -> pygame.math.Vector2:
	"""Find the exact collision point using binary search.

	Args:
		displacement: Displacement vector

	Returns:
		Position just before collision occurs
	"""

	low: float = 0.0
	high: float = 1.0
	epsilon: float = 0.001  # Precision threshold
	start_pos: pygame.math.Vector2 = pygame.math.Vector2(playground_object.m_pos)
	best_pos: pygame.math.Vector2 = pygame.math.Vector2(start_pos)

	# Binary search for collision point
	while high - low > epsilon:
		mid: float = (low + high) / 2.0
		test_pos: pygame.math.Vector2 = start_pos + (displacement * mid)

		# Temporarily set position for testing
		old_pos: pygame.math.Vector2 = pygame.math.Vector2(playground_object.m_pos)
		playground_object.m_pos = test_pos
		playground_object.update_center_depending_on_pos()

		# Check if this position causes collision
		collision_type: CollisionType = check_collisions(playground_object)

		if collision_type == CollisionType.NO_COLLISION:
			# No collision at this point, can move further
			low = mid
			best_pos = pygame.math.Vector2(test_pos)
		else:
			# Collision detected, need to move back
			high = mid

		# Restore old position
		playground_object.m_pos = old_pos
		playground_object.update_center_depending_on_pos()

	return best_pos