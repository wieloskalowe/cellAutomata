
from ..rule import Rule 
from ..ruleMask import RuleMask

class Numeric1DRule(Rule):
	def __init__(self, ruleNumeric, transitionResult):
		if ruleNumeric > 7 or ruleNumeric < 0:
			raise ValueError('Value of numeric rule has to by in range <0,7>!')

		mask = list(bin(ruleNumeric))[2::]
		

		mask = (['0']*(3-len(mask)))+mask
		mask = [d=='1' for d in mask]

		super().__init__(RuleMask(mask))
		self.transitionResult = transitionResult

	@staticmethod
	def generateRuleSet(ruleNumeric):
		if ruleNumeric > 255 or ruleNumeric < 0:
			raise ValueError('Value of numeric rule has to by in range <0,255>!')

		ret = []

		res = list(bin(ruleNumeric))[2::]
		res = (['0']*(8-len(res)))+res
		res = [r=='1' for r in res[::-1]]


		for n in range(8):
			if bool(res[0]) != bool(0x02&n):
				ret.append(Numeric1DRule(n, res[0]))
			res = res[1::]

		return tuple(ret)

	def curr_transition(self, current_cell):
		current_cell.update({'state':self.transitionResult})


	def nhbr_feature_check(self, current_cell, neighbour_cell):
		return neighbour_cell.get('state')


