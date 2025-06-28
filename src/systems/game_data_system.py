import os

class GameDataSystem:
	def __init__(self):
		self.m_save_directory = "saves"
		self.m_save_filename = "game_save.json"
		self.ensure_save_directory()

	def ensure_save_directory(self):
		if not os.path.exists(self.m_save_directory):
			os.makedirs(self.m_save_directory)

	def has_save_file(self):
		save_path = os.path.join(self.m_save_directory, self.m_save_filename)
		return os.path.exists(save_path)