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

function setNewRule(ruleName, success_handler, error_handler = logErrorResponse )
{
	issueCmd(['RULE NEW PREDEFINED', ruleName].join(' '), success_handler, error_handler)
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

function setNeighboursRadius(radius, success_handler, error_handler = logErrorResponse )
{
	issueCmd(['RADIUS', Number(radius)].join(' '), success_handler, error_handler)
}

function ruleInfo(ruleName, success_handler, error_handler = logErrorResponse)
{
	issueCmd(['RULE QUERY PREDEFINED', ruleName].join(' '), success_handler, error_handler)
}

function montecarloStep(kt, success_handler, statesOnly = true, error_handler = logErrorResponse)
{
	issueCmd(['MCST', (statesOnly ? 'STATES_ONLY' : '') , Number(kt)].join(' '), success_handler, error_handler)
}

function drxStep( success_handler, dt=0.001, ResetDRX = false, A = 86710969050178.5, B=9.41268203527779, crit=4215840142323.42, meanRatio=0.3, cannonRatio=0.0001, error_handler = logErrorResponse)
{
	issueCmd(['DRX', (ResetDRX ? 'RESET' : ''), Number(A), Number(B), Number(crit), Number(dt), Number(meanRatio), Number(cannonRatio)].join(' '), success_handler, error_handler)
}