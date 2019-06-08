from .cell import Cell

import math

class Grid:


	def __init__(self,x,y,z, requiredCellsFields = {}, sqRadius = 1):
		self.cells = []
		self.wrap = True
		self.dimension = 0
		self.sqRadius  = int(math.ceil(sqRadius))

		self.create(x,y,z, requiredCellsFields, sqRadius)
		

	
	def _idxToXYZ(self, idx):
		xdiv = (self.xs, 1)[self.xs==0]
		ydiv = (self.ys, 1)[self.ys==0]

		zi = (idx//(xdiv * ydiv))
		layerless = idx-(zi*self.xs*self.ys)
		yi = layerless//self.xs
		xi = layerless%self.xs

		return xi, yi, zi

	def _XYZtoIdx(self, x, y, z):
		x=x%self.xs
		if self.ys==0:	y = 0
		else:			y=y%self.ys;

		if self.zs==0:  z=0
		else:			z=z%self.zs

		return x+self.xs*y+(self.ys*self.xs)*z

		 

	def _determine_neighbours(self, cellIdx):
		neighbours = []

		xi, yi, zi = self._idxToXYZ(cellIdx)


		startZ = zi-self.sqRadius
		startY = yi-self.sqRadius
		startX = xi-self.sqRadius


		if self.wrap:
			if startX < 0: startX = self.xs+startX
			if startY < 0: startY = self.ys+startY
			if startZ < 0: startZ = self.zs+startZ

		
		for z in range(2*self.sqRadius+1):
			for y in range(2*self.sqRadius+1):
				for x in range(2*self.sqRadius+1):

					currX = startX + x
					currY = startY + y
					currZ = startZ + z

					if currX < 0 or currY < 0 or currZ < 0:
						neighbours.append(None)
						continue

					if not self.wrap:
						if (currX >= self.xs and self.xs >0) or\
						   (currY >= self.ys and self.ys >0) or\
						   (currZ >= self.zs and self.zs >0) :
							neighbours.append(None)
							continue


				

					neighbours.append(self._XYZtoIdx(currX,currY,currZ))

		
		return tuple(neighbours)

	def _update_edge_neighbours(self):

		toUpdate = []

		if not self.cells:
			return

		if self.dimension == 1:
			try:
				toUpdate.append(self.cells[0])
				toUpdate.append(self.cells[-1])
			except IndexError as e:
				pass


		if self.dimension == 2:
			for x in range(self.xs) : toUpdate.append(self.cells[self._XYZtoIdx(x, 0, 0)])
			for x in range(self.xs) : toUpdate.append(self.cells[self._XYZtoIdx(x, self.ys-1, 0)])

			for y in range(self.ys) : toUpdate.append(self.cells[self._XYZtoIdx(0, y, 0)])
			for y in range(self.ys) : toUpdate.append(self.cells[self._XYZtoIdx(self.xs-1, y, 0)])

		if self.dimension == 3:
			#front wall
			for x in range(self.xs) :
				for y in range(self.ys) :
					toUpdate.append(self.cells[self._XYZtoIdx(x, y, 0)])


			#back wall
			for x in range(self.xs) :
				for y in range(self.ys) :
					toUpdate.append(self.cells[self._XYZtoIdx(x, y, self.zs-1)])


			#top wall
			for x in range(self.xs) :
				for z in range(self.ys) :
					toUpdate.append(self.cells[self._XYZtoIdx(x, 0, z)])


			#bottom wall
			for x in range(self.xs) :
				for z in range(self.ys) :
					toUpdate.append(self.cells[self._XYZtoIdx(x, self.ys-1, z)])

			#left wall
			for z in range(self.zs) :
				for y in range(self.ys) :
					toUpdate.append(self.cells[self._XYZtoIdx(0, y, z)])

			#right wall
			for z in range(self.zs) :
				for y in range(self.ys) :
					toUpdate.append(self.cells[self._XYZtoIdx(self.xs-1, y, z)])


		for c in toUpdate:
			c.setNeighbours( self._determine_neighbours(c.selfId), self.sqRadius)

	def setWrapMode(self, wrap):
		self.wrap = wrap
		self._update_edge_neighbours()

	def setSqRadius(self, sqRadius):
		if self.sqRadius == sqRadius:
			return

		self.sqRadius = int(math.ceil(sqRadius))

		for n,c in enumerate(self.cells):
			c.setNeighbours( self._determine_neighbours(n), self.sqRadius )


	def create(self, x, y, z, requiredCellsFields = {}, sqRadius=1):
		if x <= 0:
			raise ValueError('X dimension has to be greater than 0!')
		if y < 0:
			raise ValueError('Y dimension has to be greater or equal 0!')
		if z < 0:
			raise ValueError('Z dimension has to be greater or equal 0!')

		if z > 0 and y <= 0:
			raise ValueError('Y dimension cannot be 0 if Z is greater than 0!')

		if sqRadius < 1:
			raise ValueError('sqRadius cannot be lower than 1!')

		self.xs = x
		self.ys = y
		self.zs = z
		self.sqRadius = int(math.ceil(sqRadius))

		self.dimension = sum(v>0 for v in [x,y,z])

		x = (x,1)[x==0]
		y = (y,1)[y==0]
		z = (z,1)[z==0]

		for n in range(x*y*z):
			tmp = Cell()
			tmp.selfId = n
			self.cells.append(tmp)

		for n,c in enumerate(self.cells):
			c.setNeighbours( self._determine_neighbours(n), self.sqRadius )



	