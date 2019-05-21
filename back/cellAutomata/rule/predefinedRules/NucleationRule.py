from ..rule import Rule 

import sys
sys.path.append('../../')

from utils import *

class NucleationRule(Rule):


	def __init__(self):
		super().__init__(Rule.createEmptyRuleMask(2))
		self.requiredCellsFields = {'state':rrange(0, None)}


	def curr_transition(self, current_cell):
		pass

	def nhbr_feature_check(self, current_cell, neighbour_cell):
		pass

	def apply(self, curr, neighbours):
		if curr['state'] != 0:
			return

		hist = {}
		
		for nc in neighbours:
			if nc is None or curr == nc:
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

		print(dominantState)
		if dominantState != 0:
			curr['state'] = dominantState

