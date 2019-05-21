from .cell import Cell
from .grid import Grid
from .rule.rule import Rule


class Simulation:


	def __init__(self):
		self._clear()

	def _clear(self, preserveWrap = False):
		self.stepCnt 	= 0
		self.grid 	 	= None
		self.rules 		= ()
		self.reqFields 	= {}

		if not preserveWrap:
			self.wrap = True
		

	def _initCellsProperities(self):
		self.reqFields = {}

		for n in self.rules:
			self.reqFields.update(n.requiredCellsFields.copy())

		if 'state' not in self.reqFields:
			self.reqFields.update({'state':(0,1)})

		for c in self.grid.cells:
			for rf in self.reqFields:
				if rf not in c:
					c.update({rf:self.reqFields[rf][0]})




	def new(self, x_size, y_size, z_size, *rules, preserveWrap = False):
		self._clear(preserveWrap)
		self.grid = Grid(x_size,y_size,z_size)
		self.grid.setWrapMode(self.wrap)
		self.setRules(rules)
		

	def step(self):
		
		if len(self.rules) <= 0:
			raise RuntimeError('Cannot perform step of simulation. No rules has been specified!')

		if self.grid is None:
			raise RuntimeError("Cannot perform step of simulation. Grid is not initialized, call method 'new()' first!")
		


		new_cells = []
		prev_cells = self.grid.cells

		t = 0
		for r in self.rules:
			if r.mask.dimension >  self.grid.dimension:
					raise RuntimeError('Mask dimension cannot be grater than dimension of the grid!')

		for c in prev_cells:
			new_cell = c.copy()
			for r in self.rules:

				
				curr_neigh = []

				for nc in new_cell.neighbours[r.mask.dimension]:
					if nc is None:
						curr_neigh.append(None)
					else:
						curr_neigh.append(prev_cells[nc])


				r.apply(new_cell, curr_neigh)

			new_cells.append(new_cell)

		print('asd')

		self.grid.cells = new_cells
		self.stepCnt=self.stepCnt+1


		return self.stepCnt, prev_cells

	def snapshot(self):
		if self.grid is None:
			raise RuntimeError("Cannot take a snapshot. Grid is not initialized, call method 'new()' first!")

		r = []
		for c in self.grid.cells:
			r.append(dict(c).copy())

		return r

	def setRules(self, *args):

		lst = [ l for l in args if type(l) is not tuple]
		
		for i,a in enumerate(lst):
			if not issubclass(type(a), Rule):
				raise ValueError("All rules passed to simulation have to inherit from 'Rule' class! Error at rule: [%d] with type '%s'" % (i, str(type(a))))

		self.rules = tuple(lst)

		if self.grid:
			self._initCellsProperities()
