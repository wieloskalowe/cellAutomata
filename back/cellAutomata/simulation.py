from .cell import Cell
from .grid import Grid
from .rule.rule import Rule

import random
import math

class Neighborhood(list):
	def __init__(self, radius = 0):
		self.inRadius = radius




class Simulation:


	def __init__(self):
		self._clear()

	def _clear(self, preserveWrap = False, preserveRadius = False):
		self.stepCnt 	= 0
		self.grid 	 	= None
		self.rules 		= ()
		self.reqFields 	= {}

		self.resetMC()
		self.resetDRX()

		if not preserveRadius:
			self.sqRadius 	= 1

		if not preserveWrap:
			self.wrap = True

	def resetMC(self):
		self.MCpool		= []
		self.MCpoolTail = -1

	def resetDRX(self):
		self.drxTime	  = 0
		self.drxStepCnt   = 0
		self.prevDrxValue = 0
		

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




	def new(self, x_size, y_size, z_size, *rules, preserveWrap = False, preserveRadius=False):
		self._clear(preserveWrap, preserveRadius)
		self.grid = Grid(x_size,y_size,z_size, sqRadius=self.sqRadius)
		self.grid.setWrapMode(self.wrap)
		self.setRules(rules)
		

	def step(self):
		
		if len(self.rules) <= 0:
			raise RuntimeError('Cannot perform step of simulation. No rules has been specified!')

		if self.grid is None:
			raise RuntimeError("Cannot perform step of simulation. Grid is not initialized, call method 'new()' first!")
		

		curr_neighs =  ( None, Neighborhood(self.sqRadius), Neighborhood(self.sqRadius), Neighborhood(self.sqRadius)  )


		for n in range(1, 4):
			for l in range((self.grid.sqRadius*2+1)**n):
				curr_neighs[n].append(None)



		new_cells = []
		prev_cells = self.grid.cells

		for r in self.rules:
			if r.mask.dimension >  self.grid.dimension:
					raise RuntimeError('Mask dimension cannot be grater than dimension of the grid!')

		for c in prev_cells:
			new_cell = c.copy()
			for r in self.rules:

				
				
				for i, nc in enumerate(new_cell.neighbours[r.mask.dimension]):
					if nc is None:
						curr_neighs[r.mask.dimension][i] = None
					else:
						curr_neighs[r.mask.dimension][i] = prev_cells[nc]


				r.apply(new_cell, curr_neighs[r.mask.dimension])



			new_cells.append(new_cell)


		self.grid.cells = new_cells
		self.stepCnt=self.stepCnt+1


		return self.stepCnt, prev_cells

	def montecarloStep(self, kt):


	

		if self.grid is None:
			raise RuntimeError("Cannot perform step of Monte carlo. Grid is not initialized, call method 'new()' first!")

		if len(self.rules) <= 0:
			raise RuntimeError('Cannot perform step of simulation. No rules has been specified!')


		if not self.MCpool:
			for c in self.grid.cells:
				if c['state'] != 0:
					self.MCpool.append(c)
			self.MCpoolTail = len(self.MCpool)-1


		if len(self.MCpool) < len(self.grid.cells):
			self.MCpool = []
			self.MCpoolTail = -1
			
			raise RuntimeError('Nucleation simulation is not done yet, cannot perform step off Monte Carlo!')

			

		if self.MCpoolTail < 0:
			raise RuntimeError('Monte carlo done!')

		for r in self.rules:
			if r.mask.dimension >  self.grid.dimension:
					raise RuntimeError('Mask dimension cannot be grater than dimension of the grid!')


		curr_neighs =  ( None, Neighborhood(self.sqRadius), Neighborhood(self.sqRadius), Neighborhood(self.sqRadius)  )
		for n in range(1, 4):
			for l in range((self.grid.sqRadius*2+1)**n):
				curr_neighs[n].append(None)


		MCidx = random.randint(0, self.MCpoolTail)
		consideredCell = self.MCpool[MCidx]

		self.MCpool[MCidx], self.MCpool[self.MCpoolTail] =  self.MCpool[self.MCpoolTail], self.MCpool[MCidx]
		self.MCpoolTail-=1

		for i, nc in enumerate(consideredCell.neighbours[r.mask.dimension]):
			if nc is None:
				curr_neighs[r.mask.dimension][i] = None
			else:
				curr_neighs[r.mask.dimension][i] = self.grid.cells[nc]


		
		for r in self.rules:
			prevState = consideredCell['state']
			neighHist = {}

		
			for n in r.filtered(curr_neighs[r.mask.dimension], consideredCell):
				if n is None: 
					continue;

				neighHist.update({n['state']:neighHist.get(n['state'], 0)+1})

			neighCnt=len(consideredCell.neighbours[r.mask.dimension])-1
			Ebefore = neighCnt-neighHist[ prevState ]

				

			while neighHist:
				Eafter 	= 0


				newState = prevState
				while newState == prevState:
					newState = random.choice(list(neighHist.keys()))
					Eafter = neighCnt-neighHist[ newState ] 

					if len(neighHist) == 1:
						del neighHist[newState]
						break
				

				if not neighHist:
					break


				if (Eafter - Ebefore) <= 0 or (random.random() <= math.exp(- ((Eafter - Ebefore)/kt) )):
					consideredCell['state'] = newState
					break

				del neighHist[newState]


				



		return self.grid.cells


	def _onEdge(self, cell):
		for c in cell.neighbours[3]:
			if c is None: continue
			c = self.grid.cells[c]

			if c['state'] != cell['state']:
				return True
		else:
			return False

	def _setRXed(self, cell, rxState):
		cell['rx'] = rxState
		cell['rxv'] = 0
		cell['rxs']	= self.drxStepCnt

	def _drxCrit(self, cell, crit):
		if cell.get('rxv', 0) < crit:
			return

		if self._onEdge(cell):
			self._setRXed(cell, 1) #recrystalized, and display
		else:
			self._setRXed(cell, 2) # recrystalized do not display
	
	def _drxTransition(self, cell):

		hasPrev 	= False

		for n in cell.neighbours[3]:
			if n is None: continue
			n = self.grid.cells[n]

			if n['rx'] > 0 and n['rxs'] == self.drxStepCnt-1: hasPrev = True
			if n['rxv'] > cell['rxv'] and n['rx'] <= 0: return


		if hasPrev:
			cell['rx'] 		= 1
			cell['rxv']  	= 0
			cell['rxs'] 	= self.drxStepCnt





	def drxStep(self, A = 86710969050178.5, B=9.41268203527779, crit=4215840142323.42, dt=0.001, meanRatio=0.3, cannonRatio=0.0001):



		ro = lambda A, B, t: (A/B)+(1-(A/B))*math.exp(-B*t) 

		if self.grid is None:
			raise RuntimeError("Cannot perform step of DRX. Grid is not initialized!")

		if meanRatio < 0 or meanRatio > 1:
			raise ValueError('Mean ratio has to be in range <0,1>')

		if cannonRatio < 0 or cannonRatio > 1:
			raise ValueError('Cannon ratio has to be in range <0,1>')

		for c in self.grid.cells:
			if c['state'] == 0:
				raise RuntimeError("Cannot perform step of DRX. Nucleation is not done!")


		crit /= len(self.grid.cells)
		self.drxStepCnt +=1;

		if self.drxStepCnt == 1:
			for c in self.grid.cells:
				c.update({'rx':0});		# 0 - not recrystalized; 1 - recrystalized, and display; 2 - recrystalized do not display
				c.update({'rxv':0});
				c.update({'rxs':0});

		

		if self.prevDrxValue == 0:
			self.prevDrxValue = ro(A, B, self.drxTime)
		
		prevTime = self.drxTime
		self.drxTime += dt;
		currDRX 	=  ro(A, B, self.drxTime)
		deltaDRX	=  currDRX-self.prevDrxValue
		

		if self.drxStepCnt == 1: return prevTime, self.prevDrxValue

		self.prevDrxValue = currDRX



		addToEach = meanRatio*(deltaDRX/len(self.grid.cells))
		rdxLeft   = (1-meanRatio)*deltaDRX

		for c in self.grid.cells:
			c.update({'rxv':c.get('rxv', 0)+addToEach})
			self._drxCrit(c, crit)


		rdxPackage 	= cannonRatio*rdxLeft;
		rdxPackagesCnt = rdxLeft/rdxPackage



		while rdxPackagesCnt > 0:
			consideredCell = self.grid.cells[random.randint(0, len(self.grid.cells)-1)]

			if self._onEdge(consideredCell): 

				if random.random() < 0.8:
					consideredCell['rxv'] = consideredCell.get('rxv', 0) + rdxPackage
					if consideredCell['rxv'] >= crit:
						self._setRXed(consideredCell, 1)

					rdxPackagesCnt-=1;

			elif random.random() < 0.2:
				consideredCell['rxv'] = consideredCell.get('rxv', 0) + rdxPackage
				if consideredCell['rxv'] >= crit:
					self._setRXed(consideredCell, 2)

				rdxPackagesCnt-=1;




		for c in self.grid.cells:
			self._drxTransition(c)

		return prevTime, self.prevDrxValue






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

	def setRadius(self, r):
		if r < 1:
			raise ValueError("Specified radius cannot be lower than 1!");


		#for i, rule in enumerate(self.rules):
		#	if r not in rule.compatibleRadius:
		#		raise ValueError("Specified radius is not compatible with rule '%s' at index [%d]" % (str(type(rule).__name__), i));

		self.sqRadius = r

		if self.grid:
			self.grid.setSqRadius(r)
