import pygame 
import sys
from player import Player
from random import choice, randint
from laser import Laser
from hamster import Hamster
import threading
import obstaculo
import time

colorcito=0;

threading_local = threading.local()

class Game:
	def __init__(self):
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)
		
		self.vidas = 3
		self.vida_surf = pygame.image.load('grafi/vida.png').convert_alpha()
		self.vida_x_start_pos = screen_width - (self.vida_surf.get_size()[0] * 2 + 20)
		self.puntaje = 0 
		self.font = pygame.font.Font('font/Pixeled.ttf',20)
		 
		self.hamsters = pygame.sprite.Group()
		self.hamster_lasers = pygame.sprite.Group() 
		self.th1 =threading.Thread(self.hamster_setup(rows = 1, cols = 8))
		self.th1.start()
		self.th2 =threading.Thread(self.hamster_setup(rows = 2, cols = 8))
		self.th2.start()
		self.th3 =threading.Thread(self.hamster_setup(rows = 3, cols = 8))
		self.th3.start()
		self.th4 =threading.Thread(self.hamster_setup(rows = 4, cols = 8))
		self.th4.start()

		#bloques
		self.shape = obstaculo.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstaculo_amount = 4
		self.obstaculo_x_positions = [num * (screen_width / self.obstaculo_amount) for num in range(self.obstaculo_amount)]
		self.create_multiple_obstaculos(*self.obstaculo_x_positions, x_start = screen_width / 15, y_start = 480)

		#musica y sonido
		music = pygame.mixer.Sound('audio/intro.wav')
		music.set_volume(0.1)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.1)
		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.4)

	##Hamsters

	def hamster_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		#for row_index, row in enumerate(range(rows)):
			row_index=rows
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index % 2==0:
					self.hamster_direc = 1
					colorcito = 1
					hamster_sprite= Hamster('rojo',x,y)
					
				else:
					self.hamster_direc=-1
					colorcito=0
					hamster_sprite= Hamster('verde',x,y)
					
				self.hamsters.add(hamster_sprite)

	def hamster_posicion_c(self):
		for hamster in self.hamsters.sprites():
			if hamster.rect.right >= screen_width:
				self.hamster_direc = -1
				self.hamster_mover_abajo(2)
			elif hamster.rect.left <= 0:
				self.hamster_direc = 1
				self.hamster_mover_abajo(2)
	

	def hamster_mover_abajo(self,distance):
		if self.hamsters:
			for hamster in self.hamsters.sprites():
				hamster.rect.y += distance
	
	def hamster_shoot(self):
		if self.hamsters.sprites():
			random_hamster = choice(self.hamsters.sprites())
			laser_sprite = Laser(random_hamster.rect.center,6,screen_height)
			self.hamster_lasers.add(laser_sprite)
			self.laser_sound.play()

	def create_obstaculo(self, x_start, y_start,offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstaculo.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_multiple_obstaculos(self,*offset,x_start,y_start):
		for offset_x in offset:
			self.create_obstaculo(x_start,y_start,offset_x)
	################################################3
	def coliciones_veri(self):

		# jugador disparo 
		if self.player.sprite.laser:
			for laser in self.player.sprite.laser:
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
					

				# hamster colicioness
				hamsters_hit = pygame.sprite.spritecollide(laser,self.hamsters,True)
				if hamsters_hit:
					for hamster in hamsters_hit:
						self.puntaje += hamster.value
					laser.kill()
					self.explosion_sound.play()
				
		# hamster lasers 
		if self.hamster_lasers:
			for laser in self.hamster_lasers:
				# obstaculo collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()

				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.vidas -= 1

						
					
		# hamsters
		if self.hamsters:
			for hamster in self.hamsters:
				pygame.sprite.spritecollide(hamster,self.blocks,True)

				if pygame.sprite.spritecollide(hamster,self.player,False):
					pygame.quit()
					sys.exit()
	#########################################

	def perder(self):
		if self.vidas <= 0:
			pygame.quit()
			sys.exit()

	def display_vidas(self):
		for vida in range(self.vidas - 1):
			x = self.vida_x_start_pos + (vida * (self.vida_surf.get_size()[0] + 10))
			screen.blit(self.vida_surf,(x,8))

	def display_puntaje(self):
		puntaje_surf = self.font.render(f'puntaje: {self.puntaje}',False,'white')
		puntaje_rect = puntaje_surf.get_rect(topleft = (10,-10))
		screen.blit(puntaje_surf,puntaje_rect)

	def ganaste_message(self):
		if not self.hamsters.sprites():
			ganaste_surf = self.font.render('Ganaste el burrito uwu!',False,'white')
			ganaste_rect = ganaste_surf.get_rect(center = (screen_width / 2, screen_height / 2))
			screen.blit(ganaste_surf,ganaste_rect)
	

	

	def run(self):
		self.player.update()
		self.hamster_lasers.update()
		self.hamsters.update(self.hamster_direc)
		self.hamster_posicion_c()
		self.coliciones_veri()
		

		self.blocks.draw(screen)

		self.player.sprite.laser.draw(screen)
		self.player.draw(screen)
		self.hamsters.draw(screen)
		
		self.hamster_lasers.draw(screen)

		self.display_vidas()
		self.display_puntaje()
		self.ganaste_message()
		self.perder()
	

class GENERADORTV:
	def __init__(self):
		self.tv = pygame.image.load('grafi/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(screen_height / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)

	def draw(self):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		screen.blit(self.tv,(0,0))

if __name__ == '__main__':
	
	pygame.init()
	screen_width = 600
	screen_height = 600
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()
	generador = GENERADORTV()

	HAMSTERLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(HAMSTERLASER,800)
	
	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == HAMSTERLASER:
					game.hamster_shoot()

		screen.fill((30,30,30))
		game.run()
		generador.draw()
			
		pygame.display.flip()
		clock.tick(60)