from ..rule import Rule 

class MooreRule(Rule):


	def __init__(self):
		super().__init__(Rule.createEmptyRuleMask(2))

	def curr_transition(self, current_cell):
		pass

	def nhbr_feature_check(self, current_cell, neighbour_cell):
		pass

	def apply(self, curr, neighbours):
		alive = 0
		
		for nc in neighbours:
			if nc is None or curr == nc:
				continue

			if nc.get('state'):
				alive=alive+1


		if alive == 3:
			curr['state'] = True

		if alive > 3 or alive < 2:
			curr['state'] = False
