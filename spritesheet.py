import pygame

class SpriteSheet():
	def __init__(self, image, x, y, scale):
		self.sheet = image
		self.sizeX = x
		self.sizeY = y
		self.scale = scale

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image