# Snake Game implementando el algoritmo A*
# Renzo Mondragon
# Joaquin Aguirre
# Francesco Bassino

import pygame
import time
from astar import Node, Board

class Game():
	def __init__(self, height=30, width=30):	
		# Iniciamos el tablero
		self.gameBoard = Board(height,width)

		# Definimos la velocidad como fps
		self.fps = 40

		# Definimos los colores
		self.backgroundColor = (0, 0, 0)
		self.snakeColor = (125, 255, 125) # Light Green
		self.headColor = (0, 143, 57) # Dark Green
		self.scoreColor = (255,255,255)
		self.foodColor = (255, 0, 0) # Red
		self.pathColor = (255,246,143) # Yellow
		self.sizeSquared = 20
		
		self.height = self.sizeSquared * self.gameBoard.height
		self.width = self.sizeSquared * self.gameBoard.width
		self.size = (self.width, self.height+100)

		self.screen = pygame.display.set_mode(self.size)
		pygame.init()
	
	def drawBoard(self):
		#myFont = pygame.font.SysFont("monospace", 50)
		self.screen.fill(self.backgroundColor)
		for i in range(self.gameBoard.height):
			for j in range(self.gameBoard.width):
				# Revisar los tipos de casillero que hay
				if self.gameBoard.board[i, j] == 1:
					tam_loc = (j*self.sizeSquared, i*self.sizeSquared, self.sizeSquared, self.sizeSquared)
					pygame.draw.rect(self.screen, self.snakeColor, tam_loc)
				elif self.gameBoard.board[i, j] == 2:
					tam_loc = (j*self.sizeSquared, i*self.sizeSquared, self.sizeSquared, self.sizeSquared)
					pygame.draw.rect(self.screen, self.headColor, tam_loc)
				elif self.gameBoard.board[i, j] == 3:
					loc = (int((j+0.5)*self.sizeSquared), int((i+0.5)*self.sizeSquared))
					pygame.draw.circle(self.screen, self.foodColor, loc, self.sizeSquared//2)
				elif self.gameBoard.board[i, j] == 4:
					tam_loc = (j*self.sizeSquared, i*self.sizeSquared, self.sizeSquared, self.sizeSquared)
					pygame.draw.rect(self.screen, self.pathColor, tam_loc)
		
		label = pygame.font.SysFont("monospace", 50).render(f"Score: {self.gameBoard.score}", 1, self.scoreColor)
		self.screen.blit(label, (self.width -580,630))
		tam_loc = (self.width, 0, 3, self.height)
		pygame.draw.rect(self.screen, (255, 255, 255), tam_loc)
		pygame.display.update()

	# Correr el juego
	def runGame(self, ai=True):
		# Loop principal del juego
		exitPressed = False
		while exitPressed == False and self.gameBoard.gaming == True:
			# Input del usuario con las teclas
			move = self.gameBoard.direction
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exitPressed = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						move = [-1, 0]
					elif event.key == pygame.K_DOWN:
						move = [1, 0]
					elif event.key == pygame.K_LEFT:
						move = [0, -1]
					elif event.key == pygame.K_RIGHT:
						move = [0, 1]
					elif event.key == pygame.K_q:
						self.gameBoard.gaming = False

			# Controlar la velocidad del juego
			time.sleep(1.0/self.fps)

			# Comprueba si la inteligencia artificial esta activada o no
			if ai:
				move = self.gameBoard.aStar() or self.gameBoard.revAStar()
			self.gameBoard.updateDirection(move)
			self.gameBoard.updateState()

			# Dibujar el tablero
			self.drawBoard()
			pygame.display.update()
				
		# Game Over
		label = pygame.font.SysFont("monospace", 40).render(f"Game Over!", 1, self.foodColor)
		self.screen.blit(label, (self.width -240,640))
		pygame.display.update()
		while exitPressed == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exitPressed = True

		# Cerrar PyGame 
		pygame.quit()


# Probando el juego
if __name__ == "__main__":
	Sneikii = Game()
	Sneikii.runGame()