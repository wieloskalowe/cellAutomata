from ..rule import * 
from enum import Enum



class NeumannRule(Rule):

	def __init__(self):
		super().__init__(Rule.createEmptyRuleMask(2))
		self.requiredCellsFields = {'state':rrange(0, None)}

		self.FILTER = [  
						   1,
						 3,4,5,
						   7
					  ] 

	def curr_transition(self, current_cell):
		pass

	def nhbr_feature_check(self, current_cell, neighbour_cell):
		pass

	def apply(self, curr, neighbours):
		if curr['state'] != 0:
			return

		hist = {}
		for nc in self.filtered(neighbours, curr):
			if nc is None:
				continue

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


