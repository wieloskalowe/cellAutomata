from ..rule import * 
from enum import Enum
import random


class HexType(Enum):
	
	LEFT	= 0
	RIGHT	= 1
	RANDOM	= 2

class HexRule(Rule):
	POSSIBLE_FILTERS = [
						[  1,2,
						 3,4,5,
						 6,7],  #LEFT

						[0,1,
						 3,4,5,
						   7,8], #RIGHT
						]

	def __init__(self, ruleType = HexType.RANDOM):
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

		self.FILTER = []

		if self.ruleType == HexType.RANDOM.value:
			if curr.get('hexFilter', None) is None:
				curr.update({'hexFilter': random.randint(0, len(HexRule.POSSIBLE_FILTERS)-1) })

			self.FILTER = HexRule.POSSIBLE_FILTERS[ curr['hexFilter'] ]
		else:
			self.FILTER = HexRule.POSSIBLE_FILTERS[self.ruleType]

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


