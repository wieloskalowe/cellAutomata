from ..rule import * 
from enum import Enum
import random



class PentagonalType(Enum):
	
	UPPER	= 0
	LOWER	= 1
	LEFT	= 2
	RIGHT	= 3
	RANDOM	= 4

class PentagonalRule(Rule):
	POSSIBLE_FILTERS = [

						[3,4,5,
						 6,7,8], #LOWER

						[0,1,2,
						 3,4,5], #UPPER


						[1,2,
						 4,5,
						 7,8],	#RIGHT

						[0,1,
						 3,4,
						 6,7],	#LEFT


						]

	def __init__(self, ruleType = PentagonalType.RANDOM):
		self.ruleType = ruleType.value
		super().__init__(Rule.createEmptyRuleMask(2))
		self.requiredCellsFields = {'state':rrange(0, None)}


	def curr_transition(self, current_cell):
		pass

	def nhbr_feature_check(self, current_cell, neighbour_cell):
		pass

	def apply(self, curr, neighbours):
		if curr['state'] != 0:
			return

		NEIGH_FILTER = []

		if self.ruleType == PentagonalType.RANDOM.value:
			if curr.get('pentFilter', None) is None:
				curr.update({'pentFilter': random.randint(0, len(PentagonalRule.POSSIBLE_FILTERS)-1) })

			self.FILTER = PentagonalRule.POSSIBLE_FILTERS[ curr['pentFilter'] ]
		else:
			self.FILTER = PentagonalRule.POSSIBLE_FILTERS[self.ruleType]

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


