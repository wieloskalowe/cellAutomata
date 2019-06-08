COMMANDS = [
				('HELLO',{ 'switches':None, 'subCommands':None,  'arguments':[str]}),
				('NEW',{ 'switches':('STATES_ONLY'), 'subCommands':None,  'arguments':[int, int, int]}),
				('STEP',{ 'switches':('STATES_ONLY'), 'subCommands':None,  'arguments':[]}),
				('RULE',{ 'switches':('NUMERIC', 'PREDEFINED'), 'subCommands':('ADD', 'NEW', 'DELETE', 'LIST', 'LIST_KNOWN', 'QUERY'),  'arguments':[str]}),
				('SETI',{ 'switches':('STATES_ONLY'), 'subCommands':None,  'arguments':[int, str]}),
				('SETC',{ 'switches':('STATES_ONLY'), 'subCommands':None,  'arguments':[int, int, int, str]}),
				('WRAP',{ 'switches':None, 'subCommands':None,  'arguments':[int]}),
				('MCST',{ 'switches':('STATES_ONLY'), 'subCommands':None,  'arguments':[float]}), #monte carlo argument -> k
				('DRX',{ 'switches':('RESET'), 'subCommands':None,  'arguments':[float, float, float, float, float, float]}),
				('RADIUS',{ 'switches':None, 'subCommands':None,  'arguments':[float]})
			   ]

class CellularReqEntity:

	def __init__(self, serialNumber, command, subCommand, switches, arguments):
		self.sn  		= serialNumber	#int
		self.cmd 		= command 		#string UPPERCASE
		self.subCmd 	= subCommand 	#string UPPERCASE
		self.switches	= switches 		#tuple of various strings (should be UPPERCASE)
		self.arguments	= arguments 	#tuple of stuff, command dependend


class CellularReqError(Exception):

	def __init__(self, msg, serialNumber):
		super().__init__(msg)
		self.serialNumber = (-1, serialNumber)[serialNumber >= 0]



class CellularPraser:



	@staticmethod
	def parseRequest(req):
		tokens = list(filter(None, req.split(' ')))

		commandIdx   = None

		serialNumber = None
		cmd 		 = ''
		subCmd 		 = ''
		switches	 = []
		arguments	 = []

		if len(tokens) < 2:
			raise CellularReqError('Invalid request!', -1)

		try:
			serialNumber = int(tokens[0], 10)
		except ValueError as e:
			raise CellularReqError('Invalid request! Serial number has to be positive decimal value!', -1)

		if serialNumber < 0:
			raise CellularReqError('Invalid request! Serial number has to be positive decimal value!', -1)

		for i,c in enumerate(COMMANDS):
			if c[0] == tokens[1]:
				commandIdx = i
				break

		if commandIdx is None:
			raise CellularReqError("Invalid request! Unknown command '%s'!" % tokens[1], serialNumber)
		
		cmd = COMMANDS[commandIdx][0]

		tokens = tokens[2::]
		COMMAND_GRAMAR = COMMANDS[commandIdx][1]




		if     not tokens \
		   and not COMMAND_GRAMAR['subCommands']\
		   and not COMMAND_GRAMAR['arguments']:
		   return CellularReqEntity(serialNumber, cmd, None, None, None)



		if COMMAND_GRAMAR['subCommands'] and tokens[0] not in COMMAND_GRAMAR['subCommands']:
			raise CellularReqError("Invalid request! Command '%s' requires at least one of '%s' subcommands!" % (cmd, COMMAND_GRAMAR['subCommands']), serialNumber)
		elif COMMAND_GRAMAR['subCommands']:
			subCmd = tokens[0]
			tokens = tokens[1::]

		if COMMAND_GRAMAR['switches']:
			tokensLeft = []
			for s in tokens:
				if s in COMMAND_GRAMAR['switches']:
					switches.append(s)
					continue

				tokensLeft.append(s)

			tokens = tokensLeft

		if (len(tokens) != len(COMMAND_GRAMAR['arguments'])):
			raise CellularReqError("Invalid request! Command '%s' requires exacly %d argument(s)." % (cmd, len(COMMAND_GRAMAR['arguments'])), serialNumber)

		for i,at in enumerate(COMMAND_GRAMAR['arguments']):
			try:
				arguments.append(at(tokens[i]))
			except ValueError:
				raise CellularReqError("Invalid request! Argument number %d has to be of type '%s'" % (i+1, at.__name__), serialNumber)

		return CellularReqEntity(serialNumber, cmd, subCmd, switches, arguments)

"""
PROTOCOL:

NNN HELLO - server response with simulation token, when connection is lost and recovered up to 10 minutes, another HELLO will load
			saved state of previous simulation
			response: OK NNN TOKEN_HERE, not crucial maybe implement later

NNN NEW x y z [STATES_ONLY] - creates new simulation of specified size, returns initial state of cells if STATES_ONLY switch is present
							  server returns array of field 'state' for each cell so instead of array:
							   [{state:1, another_attribute:'asd'}, {state:1, another_attribute:'asd'}, {state:0, another_attribute:'asd'}]
							   [1, 1, 0] will be returend

NNN STEP [STATES_ONLY]- permforms one step of the simulation and returns state of the cells, STATES_ONLY as above

NNN RULE ADD/NEW/DELETE/LIST/QUERY NUMERIC/PREDEFINED 
	ADD 	- adds rule by name/number for 1d
	NEW 	- discards previous rules and ads new one
	DELETE	- deletes specified rule
	LIST	- lists current rules
	QUERY	- queries about rule required fields

NNN SET idx field=value [STATES_ONLY] - set cell's field on specified position to value, if STATES_ONLY is set, then
											OK server response message contains only single number of new state of cell,
											otherwise returns full cell state
 	

 
SERVER RESPONSE:
OK NNN RESP - RESP is dependent on issued command
ER NNN 'MSG'

where NNN is positive decimal number of command, server response with corresponding command number.

"""

