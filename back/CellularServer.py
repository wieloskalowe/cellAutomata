from CellularParser import *

import asyncio
import websockets

import numpy
import sys
import time

import json


from cellAutomata.simulation import Simulation
from cellAutomata.rule.predefinedRules.Numeric1DRule import *
from cellAutomata.rule.predefinedRules.MooreRule import *
from cellAutomata.rule.predefinedRules.NucleationRule import *
from cellAutomata.rule.predefinedRules.PentagonalRule import *
from cellAutomata.rule.predefinedRules.NeumannRule import *
from cellAutomata.rule.predefinedRules.HexRule import *
from cellAutomata.rule.predefinedRules.RadialRule import *
from cellAutomata.utils import *


CONSOLE_LOG = True
listenerId = 0 

"""
REMOVE LATER
		self.sn  		= serialNumber	#int
		self.cmd 		= command 		#string UPPERCASE
		self.subCmd 	= subCommand 	#string UPPERCASE
		self.switches	= switches 		#tuple of various strings (should be UPPERCASE)
		self.arguments	= arguments 	#tuple of stuff, command dependend


		function newSocket(){
    ws = new WebSocket('ws://localhost:1337')
    ws.onmessage = function(d){console.log(d.data)}
	return ws
}

Pectin

"""

#===========================#
predefinedRules = {

	'Moore'		:(MooreRule),
	'Nucleation':(NucleationRule),
	'Pentagonal':(lambda : PentagonalRule(PentagonalType.RANDOM) ),
	'Neumann' 	:(NeumannRule),
	'HexLeft' 	:(lambda : HexRule(HexType.LEFT) ), 
	'HexRight'	:(lambda : HexRule(HexType.RIGHT) ),
	'HexRand' 	:(lambda : HexRule(HexType.RANDOM) ), 
	'Radius'	:(RadialRule)
}

def _predefinedToLowercase():
	global predefinedRules
	tmp = {}
	for k in predefinedRules:
		tmp.update({k.lower():predefinedRules[k]})

	predefinedRules = tmp

_predefinedToLowercase();
#===========================#


class CellularDispatcher:

	def __init__(self):
		self.simulation 	= Simulation()
		self.activeRules	= {}

	def _getCellsStateJSON(self, statesOnly):
		ret = []
		if statesOnly:
			ret = [c.get('state', 0) for c in self.simulation.grid.cells]
		else:
			ret = [dict(c) for c in self.simulation.grid.cells]

		return json.dumps(ret)


	def _handleHELLO(self, entity):
		return self.generateError(entity.sn, "Not implemented yet...")
		pass


	def _handleNEW(self, entity):

		try:
			self.simulation.new(entity.arguments[0], entity.arguments[1], entity.arguments[2], preserveWrap=True, preserveRadius=True)
		except RuntimeError as re:
			return self.generateError(entity.sn, str(re))
		except ValueError as ve:
			return self.generateError(entity.sn, str(ve))

		STATES_ONLY =  (entity.switches is not None and 'STATES_ONLY' in entity.switches)
		return self.generateSuccess(entity.sn, self._getCellsStateJSON(STATES_ONLY))
		

	def _handleSTEP(self, entity):
		try:
			self.simulation.step()
		except RuntimeError as re:
			return self.generateError(entity.sn, str(re))
		except ValueError as ve:
			return self.generateError(entity.sn, str(ve))
		
		STATES_ONLY =  (entity.switches is not None and 'STATES_ONLY' in entity.switches)
		return self.generateSuccess(entity.sn, self._getCellsStateJSON(STATES_ONLY))


	"""
	NNN RULE ADD/NEW/DELETE/LIST/QUERY NUMERIC/PREDEFINED 
		ADD 	- adds rule by name/number for 1d
		NEW 	- discards previous rules and ads new one
		DELETE	- deletes specified rule
		LIST	- lists current rules
		QUERY	- queries about rule required fields
	"""
	def _updateSimulationRules(self):

		
		toSet = []
		for k in self.activeRules:
			toSet += self.activeRules[k]

		self.simulation.setRules(*toSet)

	@staticmethod
	def _is_ER(resp):
		return resp.split(' ', 2)[1:2:] == ['ER']

	def _handleRULE_ADD(self, entity, addHere=None, updateSimulationRules = True):

		if addHere is None:
			addHere = self.activeRules

		if len(entity.switches) != 1 :
			return self.generateError(entity.sn, 'Rule has to be NUMERIC or PREDEFINED, exacly one of them!')


		if 'NUMERIC' in entity.switches:
			try:
				ruleSet = Numeric1DRule.generateRuleSet(int(entity.arguments[0], 10))
			except ValueError as ve:
				return self.generateError(entity.sn, ve)

			addHere.update({str(entity.arguments[0]):list(ruleSet)})


		elif 'PREDEFINED' in entity.switches:

			name = entity.arguments[0].lower()	
			try:
				rule = predefinedRules[name]()
			except KeyError:
				return self.generateError(entity.sn, 'Unknown predefined rule, check spelling (matching is case insensitive)!')

			ruleSet = [ rule ]
			addHere.update({name:ruleSet})

		else:
			return self.generateError(entity.sn, 'Unknown rule switch %s need dispatcher update?.' % entity.switches)

		if updateSimulationRules:
			self._updateSimulationRules()

		return self.generateSuccess(entity.sn)



	def _handleRULE_NEW(self, entity):
		tmp = {}
		prevRules = self.activeRules
		self.activeRules = {}

		resp = self._handleRULE_ADD(entity, tmp, False)
		if self._is_ER(resp) : 
			self.activeRules = prevRules
			return resp

		self.activeRules = tmp
		self._updateSimulationRules()

		return self.generateSuccess(entity.sn)
		
		

	def _handleRULE_DELETE(self, entity):

		try:
			del self.activeRules[entity.arguments[0].lower()]
		except KeyError:
			return self.generateError(entity.sn, "No such active rule '%s'." % entity.arguments[0])

		self._updateSimulationRules()

		warn = ''
		if entity.switches:
			warn="Switch(es) '%s' has no use here!" % ' '.join(entity.switches)

		return self.generateSuccess(entity.sn, warn)


	def _handleRULE_LIST(self, entity):
		nameFilter = entity.arguments[0].lower()
		return self.generateSuccess(entity.sn, json.dumps([r for r in self.activeRules if r.find(nameFilter) >= 0 or nameFilter == '*']))

	def _handleRULE_LIST_KNOWN(self, entity):
		nameFilter = entity.arguments[0].lower()
		known = {'PREDEFINED':[], 'NUMERIC':[]}

		if 'PREDEFINED' in entity.switches or not entity.switches:
			for k in predefinedRules:
				if k.find(nameFilter) >= 0 or nameFilter == '*':
					known['PREDEFINED'].append(k)

		if 'NUMERIC' in entity.switches or not entity.switches:
			for n in range(0, 256):
				if str(n).find(nameFilter) >= 0 or nameFilter == '*':
					known['NUMERIC'].append(str(n))


		return self.generateSuccess(entity.sn, json.dumps(known))


	def _handleRULE_QUERY(self, entity):
		if len(entity.switches) != 1 :
			return self.generateError(entity.sn, 'Rule has to be NUMERIC or PREDEFINED, exacly one of them!')

		requiredFields = {'state':( 0 , 1)}
		ruleName = entity.arguments[0].lower()

		if 'NUMERIC' in entity.switches:
			try:
				ruleSet = Numeric1DRule.generateRuleSet(int(ruleName, 10))
			except ValueError as ve:
				return self.generateError(entity.sn, ve)

			requiredFields.update(ruleSet[0].requiredCellsFields)

		elif 'PREDEFINED' in entity.switches:

			try:
				rule = predefinedRules[ruleName]()
			except KeyError:
				return self.generateError(entity.sn, 'Unknown predefined rule, check spelling (matching is case insensitive)!')

			requiredFields.update(rule.requiredCellsFields)

		else:
			return self.generateError(entity.sn, 'Unknown rule switch %s need dispatcher update?.' % entity.switches)


		return self.generateSuccess(entity.sn, json.dumps(requiredFields))


	def _handleRULE(self, entity):

		try:
			return {
					'ADD':self._handleRULE_ADD,
					'NEW':self._handleRULE_NEW,
					'DELETE':self._handleRULE_DELETE,
					'LIST':self._handleRULE_LIST,
					'LIST_KNOWN':self._handleRULE_LIST_KNOWN,
					'QUERY':self._handleRULE_QUERY,
					}[entity.subCmd](entity)
		except KeyError as e:
			return self.generateError(entity.sn, "Unknown RULE subcommand '%s', need dispatcher upgrade?" % (entity.subCmd))



	def _setCellByIdx(self, idx, reqSet):
		if idx < 0:
			raise ValueError('Index cannot be negative!')

		if idx >= len(self.simulation.grid.cells):
			raise ValueError('Reference to cell out of grid range!')

		try:
			field, value = reqSet.split('=', 1)
		except ValueError as e:
			raise ValueError("Invalid data format! Expected: 'field=value'")

		cell  = self.simulation.grid.cells[idx]

		if field not in cell:
			raise ValueError('Invalid field name for specified rules!')

		try:
			value = int(value, 10)
		except ValueError as e:
			value = str(value)

		if self.simulation.reqFields and value in self.simulation.reqFields[field]:
			cell.update({field:value})
		else:
			raise ValueError("Invalid value '%s' for field '%s' with current rules set! Valid values '%s'" % (value, field, self.simulation.reqFields.get(field, tuple())))

		return dict(cell)


	def _handleSETI(self, entity):

		if self.simulation.grid is None or not self.simulation.grid:
			return self.generateError(entity.sn,"Grid is not initialized call 'NEW'!")

		try:
			cellData = self._setCellByIdx(entity.arguments[0], entity.arguments[1])
		except ValueError as e:
			return  self.generateError(entity.sn, str(e))


		if entity.switches is not None and 'STATES_ONLY' in entity.switches:
			cellData = cellData['state']


		return self.generateSuccess(entity.sn, json.dumps(cellData))
		

	def _handleSETC(self, entity):
		if self.simulation.grid is None or not self.simulation.grid:
			return self.generateError(entity.sn,"Grid is not initialized call 'NEW'!")

		labels = ['x', 'y', 'z']
		dsizes = [self.simulation.grid.xs, self.simulation.grid.ys, self.simulation.grid.zs]

		for n in range(3):
			if (entity.arguments[n] <= 0 and  dsizes[n] > 0)or \
			   (dsizes[n] == 0 and entity.arguments[n] < 0 ):
				return  self.generateError(entity.sn, "Value of '%s' dimension has to be greater of equal 0!" % labels[n])

			if entity.arguments[n] > dsizes[n]:
				return  self.generateError(entity.sn, "Value of '%s' dimension has to be lower (or equal if zero) than grid '%s' dimension (%d).!" % (labels[n], labels[n], dsizes[n]))


		idx = self.simulation.grid._XYZtoIdx(entity.arguments[0], entity.arguments[1], entity.arguments[3])

		try:
			cellData = self._setCellByIdx(idx, entity.arguments[3])
		except ValueError as e:
			return  self.generateError(entity.sn, str(e))



		if entity.switches is not None and 'STATES_ONLY' in entity.switches:
			cellData = cellData['state']

		return self.generateSuccess(entity.sn, json.dumps(cellData))

	def _handleWRAP(self, entity):
		wrap = bool(entity.arguments[0])

		self.simulation.wrap = wrap
		if self.simulation.grid:
			self.simulation.grid.setWrapMode(wrap)

		return self.generateSuccess(entity.sn, json.dumps(wrap))
		
	def _handleRADIUS(self, entity):
		r = float(entity.arguments[0])

		try:
			self.simulation.setRadius(r)
		except ValueError as e:
			return self.generateError(entity.sn, e)

		return self.generateSuccess(entity.sn, '')

	def _handleMCST(self, entity):
		try:
			self.simulation.montecarloStep(entity.arguments[0])
		except RuntimeError as re:
			return self.generateError(entity.sn, str(re))
		except ValueError as ve:
			return self.generateError(entity.sn, str(ve))
		
		STATES_ONLY =  (entity.switches is not None and 'STATES_ONLY' in entity.switches)
		return self.generateSuccess(entity.sn, self._getCellsStateJSON(STATES_ONLY))

	def _handleDRX(self, entity):

		if 'RESET' in entity.switches:
			self.simulation.resetDRX()

		try:
			time, ro = self.simulation.drxStep(*entity.arguments) 
		except RuntimeError as re:
			return self.generateError(entity.sn, str(re))
		except ValueError as ve:
			return self.generateError(entity.sn, str(ve))
		
	
		return self.generateSuccess(entity.sn, json.dumps({'time':time, 'ro':ro, 'cells':self.simulation.grid.cells}))

	#========================================#

	def generateError(self, serialNumber, msg):
		return "%d ER %s" % (serialNumber, msg)

	def generateSuccess(self, serialNumber, load = ''):
		return "%d OK %s" % (serialNumber, load)

	def dispatchRequest(self, req):

		try:
			parsedEntity = CellularPraser.parseRequest(req)
		except CellularReqError as cqr:
			return self.generateError(cqr.serialNumber, str(cqr))


		try:
			return {
					'HELLO':self._handleHELLO,
					'NEW':self._handleNEW,
					'STEP':self._handleSTEP,
					'RULE':self._handleRULE,
					'SETI':self._handleSETI,
					'SETC':self._handleSETC,
					'WRAP':self._handleWRAP,
					'RADIUS':self._handleRADIUS,
					'MCST':self._handleMCST,
					'DRX':self._handleDRX
					}[parsedEntity.cmd](parsedEntity)
		except KeyError as e:
			return self.generateError(req.sn, "Unknown command '%s', need dispatcher upgrade?" % (req.cmd))




async def listen(websocket, path):
		global listenerId
		dispatcher = CellularDispatcher()
		myId = listenerId
		listenerId+=1

		while True:
			request = await websocket.recv()
			response = ''

			if CONSOLE_LOG:
				print("Listener nr. %d Recieved request: '%s' " % (myId, request))

			response = dispatcher.dispatchRequest(request)

			if CONSOLE_LOG:
				print("Listener nr. %d Respond '%s' " % (myId, response))

			await websocket.send(response)





if __name__ == '__main__':
	start_server = websockets.serve(listen, 'localhost', 1337)
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
