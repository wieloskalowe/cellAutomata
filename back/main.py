
import numpy
import sys
import time


from cellAutomata.simulation import Simulation
from cellAutomata.rule.predefinedRules.Numeric1DRule import *
from cellAutomata.rule.predefinedRules.MooreRule import *
from cellAutomata.utils import *


OneDim=True


def main():

	s = time.time()
	simulation = Simulation()
	simulation.new(800,(100,0)[OneDim],0)
	#simulation.grid.setWrapMode(False)


	if OneDim:
		simulation.setRules(*Numeric1DRule.generateRuleSet(90))
	else:
		simulation.setRules(MooreRule());


	if OneDim:
		simulation.grid.cells[151].update({'state':True})
	else:
		simulation.grid.cells[798].update({'state':True})
		simulation.grid.cells[899].update({'state':True})
		simulation.grid.cells[997].update({'state':True})
		simulation.grid.cells[998].update({'state':True})
		simulation.grid.cells[999].update({'state':True})
	print('Init time: %f' % (time.time()- s))


	s = time.time()
	res = []
	for n in range(500):


		_, old = simulation.step()


		

		if OneDim:
			res.append([s.get('state', False) for s in old])
		else:
			res = []
			res.append([s.get('state', False) for s in old])
			graph(numpy.reshape(res, (100, 100)))

	print('Exec time: %f' % (time.time()- s))
	if OneDim:
		graph(res)


if __name__ == "__main__":
	main()
	