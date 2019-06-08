from ..rule import * 
from enum import Enum
import math



class RadialRule(Rule):


	def __init__(self):
		super().__init__(Rule.createEmptyRuleMask(2))
		self.requiredCellsFields = {'state':rrange(0, None), 'offX':RandGenerator(), 'offY':RandGenerator()}
		self.compatibleRadius	 = rrange(0, float('inf'))


	def curr_transition(self, current_cell):
		pass

	def nhbr_feature_check(self, current_cell, neighbour_cell):
		pass

	def _distance(cx, cy, nx, ny, currCell, currNeigh):

		nnx = nx + currNeigh.get('offX', 0)
		nny = ny + currNeigh.get('offY', 0)


		return (cx-nnx)**2+(nny-cy)**2

	def filtered(self, neighbours, curr=None):

		r = neighbours.inRadius**2
		width   = int(math.ceil(neighbours.inRadius))*2+1

		cx = width//2 + curr.get('offX', 0)
		cy = width//2 + curr.get('offY', 0)

		nx = 0
		ny = 0

		for n in neighbours:
			if n is None: continue;

			if RadialRule._distance(cy, cx, ny, nx, curr, n) <= r:
					yield n

			nx+=1
			nx%=width
			if nx==0: ny+=1


	def apply(self, curr, neighbours):

		if curr['state'] != 0:
			return
		
		
		width   = int(math.ceil(neighbours.inRadius))*2+1

		cx = width//2 + curr.get('offX', 0)
		cy = width//2 + curr.get('offY', 0)




		hist = {}
		for nc in self.filtered(neighbours, curr):
			if nc is None or nc == curr: continue;

			v = hist.get(nc['state'], 0)+1
			hist.update({nc['state']:v})




		dominantState = 0
		dominantCount = 0

		for k in hist:
			if k == 0: continue;
			if hist[k] > dominantCount:
				dominantState = k
				dominantCount = hist[k]

		
		if dominantState != 0:
			curr['state'] = dominantState


