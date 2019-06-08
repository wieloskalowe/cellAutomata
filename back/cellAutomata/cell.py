
class Cell(dict):
	RADIUS  = 1
	SIDE    = 3
	TWO_D_B = (SIDE**2)*(SIDE//2)
	TWO_D_E = TWO_D_B + SIDE**2
	ONE_D_B = (SIDE**2*(SIDE//2))+SIDE*(SIDE//2)
	ONE_D_E = ONE_D_B + SIDE

	def __init__(self):
		super().__init__()
		self.neighbours = [None, [],[],[]]
		self.selfId = None
		self.update({'state':0})

	def __getattribute__(self, a):
		if a not in self:
			return super().__getattribute__(a)
		else:
			return self.get(a)

	def __setattr__(self, a, v):
		if a not in self:
			return super().__setattr__(a,v)
		else:
			return self.update({a:v})


	@staticmethod
	def slice1dNeighbours(neighbours3d):
		return tuple(neighbours3d[Cell.ONE_D_B:Cell.ONE_D_E:])
		
	@staticmethod
	def slice2dNeighbours(neighbours3d):
		return tuple(neighbours3d[Cell.TWO_D_B:Cell.TWO_D_E:])

	def setNeighbours(self, neighbours3d, radius):
		if Cell.RADIUS != radius:
			Cell.RADIUS = radius
			Cell.SIDE   = radius*2+1

			Cell.TWO_D_B = (Cell.SIDE**2)*(Cell.SIDE//2)
			Cell.TWO_D_E = Cell.TWO_D_B + Cell.SIDE**2
			Cell.ONE_D_B = (Cell.SIDE**2*(Cell.SIDE//2))+Cell.SIDE*(Cell.SIDE//2)
			Cell.ONE_D_E = Cell.ONE_D_B + Cell.SIDE

		self.neighbours    = [None, [],[],[]]
		self.neighbours[3] = tuple(neighbours3d)
		self.neighbours[2] = Cell.slice2dNeighbours(neighbours3d)
		self.neighbours[1] = Cell.slice1dNeighbours(neighbours3d)
		self.neighbours = tuple(self.neighbours)

	def __eq__(self, b):
		return self.selfId == b.selfId

	def copy(self):
		cell = Cell()
		cell.selfId = self.selfId
		cell.neighbours = self.neighbours
		cell.update(self)

		return cell

