from .ruleMask import RuleMask
import abc

class Rule:

	@staticmethod
	def createEmptyRuleMask(dimension):
		if dimension < 1 and dimension > 3:
			raise ValueError('Dimension has to be in range <1,3>!')



		mask = [0*3]
		
		if dimension == 2:
			mask = [[0]*3]*3

		if dimension == 3:
			mask = [[[0]*3]*3]*3

		return RuleMask(mask)

	def __init__(self, ruleMask):
		if type(ruleMask) is not RuleMask:
			raise TypeError('Mask passed to rule constructor has to be of type RuleMask!')

		self.mask = ruleMask
		self.requiredCellsFields = {}


	@abc.abstractmethod
	def curr_transition(self, current_cell):
		pass

	@abc.abstractmethod
	def nhbr_feature_check(self, current_cell, neighbour_cell):
		pass

	@abc.abstractmethod
	def apply(self, current_cell, neighbours):
		for i, nc in enumerate(neighbours):
			if nc is None:
				if self.mask.mask[i]:
					break
				else:
					continue
			
			if not bool(self.nhbr_feature_check(current_cell, nc)) == self.mask.get(i):
				break
		else:
			self.curr_transition(current_cell)
