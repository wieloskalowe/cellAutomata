
class Cell(dict):

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
		return tuple(neighbours3d[12:15:])
		
	@staticmethod
	def slice2dNeighbours(neighbours3d):
		return tuple(neighbours3d[9:18:])

	def setNeighbours(self, neighbours3d):
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

