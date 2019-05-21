var ENABLE_NOISY_LOGGING = true
var MESSANGER_INSTANCE = null

var PREDEFINED_RULES = null

function pectin_setMessangerInstance(i)
{
	MESSANGER_INSTANCE = i
}


function logErrorResponse(d)
{
	console.error("CELLULAR SERVER ERROR RESPONSE: " + String(d))
	if(ENABLE_NOISY_LOGGING)
		alert(d)
}

function issueCmd(request, success_handler, error_handler ){
	return MESSANGER_INSTANCE.issueCmd(request, success_handler, error_handler)
}

function newNumericRule(ruleNumber, success_handler, error_handler = logErrorResponse)
{
	if(ruleNumber > 255 || ruleNumber < 0 || !Number.isInteger(ruleNumber))
		throw 'Rule number has to be integer in range <0,255>'

	issueCmd('RULE NEW NUMERIC '+String(ruleNumber), success_handler, error_handler)
}

function new1Dsimulation(size, statesOnly, success_handler, error_handler = logErrorResponse)
{
	issueCmd(['NEW', String(size), '0 0', (statesOnly ? 'STATES_ONLY' : '')].join(' '), success_handler, error_handler)
}

function new2Dsimulation(xSize, ySize, statesOnly, success_handler, error_handler = logErrorResponse)
{
	issueCmd(['NEW ', String(xSize), String(ySize), '0', (statesOnly ? 'STATES_ONLY' : '')].join(' '), success_handler, error_handler)
}


function addNamedRule(ruleName, success_handler, error_handler = logErrorResponse )
{
	issueCmd(['RULE ADD PREDEFINED', ruleName].join(' '), success_handler, error_handler)
}


function simulationStep( statesOnly, success_handler, error_handler = logErrorResponse)
{
	issueCmd(['STEP', (statesOnly ? 'STATES_ONLY' : '')].join(' '), success_handler, error_handler)
}

function setCellState(idx, newState, statesOnly, success_handler, error_handler = logErrorResponse )
{
	issueCmd(['SETI', idx, 'state='+String(newState), (statesOnly ? 'STATES_ONLY' : '')].join(' '), success_handler, error_handler)
}

function setWrappingMode(wrap, success_handler, error_handler = logErrorResponse )
{
	issueCmd(['WRAP', Number(wrap)].join(' '), success_handler, error_handler)
}

function ruleInfo(ruleName, success_handler, error_handler)
{
	issueCmd(['RULE QUERY PREDEFINED', ruleName].join(' '), success_handler, error_handler)
}