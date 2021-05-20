# Snake Game implementando el algoritmo A*
# Renzo Mondragon
# Joaquin Aguirre
# Francesco Bassino

import numpy as np
import random as rnd
import os

# Clase Nodo
class Node():
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		self.f, self.g, self.h = 0,0,0

	def __eq__(self, other):
		return self.position == other.position

# Clase Tablero
class Board():
	def __init__(self, height=15, width=15):
		# Estado de Juego
		self.gaming = True # Falso cuando es Game Over

		# Tablero
		self.height = height
		self.width  = width
		self.board  = np.zeros([self.height, self.width], dtype=int)
		self.score  = 0
		self.cost = 1

		# Direcciones
		self.inputs	 = ["w","s","a","d"]
		self.directions = [[-1,0],[0,-1],[1,0],[0,1]]
		self.direction  = rnd.Random().choice(self.directions) # Obtener una direccion aleatoria
		self.reverse	= None

		# Serpiente
		self.head  = [self.height//2, self.width//2] # Ubicar la serpiente al medio
		self.snake = [[self.head[0] - i*self.direction[0], self.head[1] - i*self.direction[1]] for i in range(3)] # Obtener coordenadas del cuerpo de la serpiente segun la posicion de la cabeza
		
		# Rellenar Tablero, 0: vacio, -1 : comida, 1 : cuerpo, 2 : cabeza
		for s in self.snake: # Ubicar la serpiente en la matriz 2d tablero
			self.board[s[0],s[1]] = 1 # board[x,y] = board[x][y]
		self.board[self.head[0], self.head[1]] = 2 # Marcar la cabeza de la serpiente en el tablero
		self.food = self.getRandomBlank()
		self.board[self.food[0], self.food[1]] = 3 # Marcar la comida de la serpiente en el tablero

		#### TEST
		self.reversa = 1
		self.temp_head_orig = []

		
	# Imprimir el tablero con la serpiente
	def __str__(self):
		os.system('cls' if os.name == 'nt' else 'clear') # Limpiar consola
		stringy = " " + "_"*self.width + "\n"
		for i in range(self.height):
			stringy += "|"
			for j in range(self.width):
				if self.board[i, j] == 2: # Cabeza
					stringy += "X"
				elif self.board[i, j] == 1: # Cuerpo
					stringy += "x"
				elif self.board[i, j] == 3: # Comida
					stringy += "O"
				elif self.board[i, j] == 4: # Camino
					stringy += "+"
				elif self.board[i, j] == 0: # Vacio
					stringy += " "
			stringy += "|\n"
		stringy += u" \u0305"*self.width + "\n" # Guion arriba
		stringy += f"Score: {self.score}" + "\n"
		return stringy
	
	# Busca espacios en desocupados y devuelve una coordenada aleatoria 
	def getRandomBlank(self):
		# Obtener un listado de ubicaciones vacias (=0)
		blanks = [[i, j] for i in range(self.height) for j in range(self.width) if self.board[i, j] == 0]
		# Elegir aleatoriamente de todas las ubicaciones vacias
		return rnd.Random().choices(blanks)[0]
	
	# Actualizar la direccion
	def updateDirection(self, direction):
		tempHead = [self.head[0] + direction[0], self.head[1] + direction[1]]
		if tempHead != self.snake[1]: # se asegura que no es una parte del cuerpo previa
			self.direction = direction
	
	# Procesar entradas de movimiento
	def processInput(self,rawInput):
		for i, move in enumerate(self.inputs):
			if rawInput == move:
				return self.directions[i]
		return self.direction
	
	# Actualizar el estado del juego
	def updateState(self):
		self.head[0] += self.direction[0]
		self.head[1] += self.direction[1]
		# Limite vertical
		if self.head[0] < 0 or self.head[0] >= self.height:
			self.head = self.snake[0].copy() # movimiento invalido
			self.gaming = False
		# Limite horizontal
		elif self.head[1] < 0 or self.head[1] >= self.width:
			self.head = self.snake[0].copy() # movimiento invalido
			self.gaming = False
		# Choca con su propio cuerpo
		elif self.head in self.snake[2::]: # serpiente en cuerpo y no hay vuelta en U
			self.head = self.snake[0].copy() # movimiento invalido
			self.gaming = False
		# Movimiento valido
		elif self.head not in self.snake:
			# Obtuvo comida
			if self.head == self.food: 
				# Aumentar el puntaje	
				self.score += 1
				# Serpiente crece, insertar posicion actual al comienzo de la lista
				self.snake.insert(0, self.head.copy()) 
				# Marcar la posicion anterior de la cabeza como cola
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				# Actualizar la posicion de la cabeza
				self.board[self.head[0], self.head[1]] = 2
				# Generar mas comida obteniendo una posicion vacia aleatoria
				self.food = self.getRandomBlank()
				# Marcar la comida en el tablero
				self.board[self.food[0], self.food[1]] = 3

			# Mover serpiente
			else: 
				self.snake.insert(0, self.head.copy())
				self.board[self.snake[1][0], self.snake[1][1]] = 1
				self.board[self.head[0], self.head[1]] = 2
				rem = self.snake.pop()
				self.board[rem[0], rem[1]] = 0
		# Movimiento invalido
		else:
			self.head = self.snake[0].copy()
	
	# Retorna el camino completo de la busqueda de A-star
	def solveAStar(self, currentNode):
		# Se explora el nodo final pasando por cada padre
		path = [] # Lista donde se guardara el camino
		current = currentNode
		while current is not None: # Hasta que ya no haya nodos padre (nodo de inicio)
			path.append(current.position)
			current = current.parent
		path = path[::-1] # Se invierte el camino porque se necesita mostrar de comienzo a final

		# El valor con el que se marcara el camino
		# Se limpia cualquier camino que se haya trazado anteriormente
		self.board = np.array([[self.board[i][j] if self.board[i][j] != 4 else 0 for j in range(self.width)] for i in range(self.height)])
		
		# Marcamos el camino en el tablero
		mark = 4
		#self.board = np.array([[self.board[i][j] if ([i,j] not in path[1:len(path)-1]) else mark for j in range(self.width)] for i in range(self.height)])
		for i in range(1,len(path)-1): # Imprimimos todo el camino excepto el primer y ultimo valor que representa inicio y final
			self.board[path[i][0]][path[i][1]] = mark
		
		# Devolvemos la direccion del primer paso
		if len(path)>1:
			return [path[1][0]-self.head[0],path[1][1]-self.head[1]]
		else:
			self.gaming = False
			return [0,0]

	# Busqueda informada de A-star
	def aStar(self, ending = None):
		# Crear nodo de comienzo y final con los valores g,h,f inicializados
		startNode = Node(None, self.head)
		endNode = Node(None, (ending or self.food)) # Revisar si el ending ha sido declarado o no

		# Iniciar las listas de visitado y por visitar
		toVisit = [] # Los que faltan visitar para explorar. Aqui se encuentra el nodo de menor costo para expandir luego
		visited = [] # Los que ya han sido explorados

		toVisit.append(startNode) # Agregamos el nodo inicial
		
		# Loop hasta que encuentre el final
		while len(toVisit) > 0:

			# Obtener el nodo a evaluar
			# Eliminar el nodo de la lista de los que faltan visitar y agregarlo a la lista de los visitados
			currentNode = toVisit.pop(0)
			visited.append(currentNode)

			# Comprobar si se ha alcanzado el destino
			if currentNode == endNode:
				return self.solveAStar(currentNode) # Retornar el camino hasta el nodo actual

			# Generar nodos hijos para todos los cuadrados adyacentes del nodo
			for direction in self.directions: # Iterar por cada direccion (arriba, abajo, derecha, izquierda)
				# Generar la nueva posicion del nodo utilizando una direccion
				nodePosition = [currentNode.position[0] + direction[0], currentNode.position[1] + direction[1]]

				# Comprobar si esta dentro de los limites del tablero
				if (nodePosition[0] > (self.height-1) or 
					nodePosition[0] < 0 or 
					nodePosition[1] > (self.width-1) or 
					nodePosition[1] < 0):
					continue

				# Comprobar si no hay obstaculos
				if self.board[nodePosition[0]][nodePosition[1]] == 1:
					continue

				# Nuevo nodo
				newNode = Node(currentNode, nodePosition)

				# Generar los valores f, g y h
				newNode.g = currentNode.g + self.cost # Aqui se podria utilizar el valor de la arista, si es que existiese
				# Coste de heuristica es calculado aqui, utilizando la distancia euclidiana
				newNode.h = (((newNode.position[0]-endNode.position[0]) ** 2) +  ((newNode.position[1]-endNode.position[1])** 2))**0.5 
				newNode.f = newNode.g + newNode.h

				# Comprobar que el nodo no esta en la lista de los visitados
				if newNode in visited:
					continue
				
				# Comprobar que el nodo no esta en la lista de los que faltan visitar
				if newNode not in toVisit:
					# Agregar el nodo hijo a la lista de los que faltan visitar
					toVisit.insert(0, newNode)
					# Ordenar la lista para que el primer nodo sea el del valor f minimo
					toVisit.sort(key = lambda x: x.f)
					# Revertir la lista para agarrar primero al que tenga el valor f maximo
					if endNode.position != self.food:
						toVisit.reverse()

	# A-Star reverso cuando no hay camino
	def revAStar(self):
		# Iniciar matrices donde se guardaran los espacios en blanco validos
		blanks, visited, toVisit = [], [], []
		# Añadir el nodo inicial a la lista por visitar
		toVisit.append(self.head)
		blanks.append(self.head)
		while len(toVisit) > 0:
			position = toVisit.pop(0)
			visited.append(position)

			for direction in self.directions:
				# Generar la nueva posicion del nodo utilizando una direccion
				newPosition = [position[0] + direction[0], position[1] + direction[1]]
				# Comprobar si esta dentro de los limites del tablero
				if (newPosition[0] > (self.height-1) or 
					newPosition[0] < 0 or 
					newPosition[1] > (self.width-1) or 
					newPosition[1] < 0):
					continue
				# Comprobar si no hay obstaculos
				if self.board[newPosition[0]][newPosition[1]] == 1:
					continue
				# Comprobar que el nodo no esta en la lista de los visitados
				if newPosition in visited:
					continue
				# Comprobar que el nodo no esta en la lista de los que faltan visitar
				if newPosition not in toVisit:
					# Agregar el nodo hijo a la lista de los que faltan visitar
					toVisit.append(newPosition)
					blanks.append(newPosition)
		
		# Escoger la posicion más lejana a la comida como el destino
		temp, near = 0, None
		for i in range(len(blanks)):
			heuristic = ((blanks[i][0]-self.food[0])**2+(blanks[i][1]-self.food[1])**2)**0.5
			#heuristic = ((blanks[i][0]-self.head[0])**2+(blanks[i][1]-self.head[1])**2)**0.5#
			if heuristic > temp:
				temp = heuristic
				near = blanks[i].copy()
		
		return self.aStar(near)

# Probando el tablero
if __name__ == "__main__":
	game = Board(30,30)
	while game.gaming:
		print(game)
		game.updateDirection(game.aStar() or game.revAStar())
		game.updateState()

	print("Game Over")
