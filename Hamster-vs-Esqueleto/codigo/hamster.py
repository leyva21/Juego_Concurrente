import pygame

class Hamster(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = 'grafi/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))
		if color == 'rojo': self.value = 3
		elif color == 'verde': self.value = 6

	def update(self,direction):
		self.rect.x += direction
